from .inputs import inputs_dict
from .well_system import set_well
from .linearsystem import calc_temperature_distribution
from .plot import plot_behavior
from scipy.interpolate import make_interp_spline
import numpy as np
import scipy.signal
import well_profile as wp


def calc_temp(trajectory, casings=None, set_inputs=None, operation='drilling', time_steps=210, smooth=True,
              cells_no=None):
    """
    Function to calculate the well temperature distribution during a specific operation at a certain time.

    Arguments:
        trajectory: wellbore trajectory excel|csv|dataframe|list
        casings: list of dictionaries with casings characteristics (od, id and depth)
        set_inputs: dictionary with parameters to set.
        operation: define operation type. ('drilling', 'circulating')
        time_steps: number of time steps to run calculations.
        smooth: smooth the temperature profiles.
        cells_no: (int) number of cells. If None -> keep same number of cells than trajectory

    Returns:
        Well temperature distribution object
    """

    tdata = inputs_dict(casings)

    if set_inputs is not None:
        for x in set_inputs:  # changing default values
            if x in tdata:
                tdata[x] = set_inputs[x]
            else:
                raise TypeError('%s is not a parameter' % x)

    if cells_no is not None:
        survey = wp.load(trajectory, points=cells_no).trajectory
    else:
        survey = wp.load(trajectory, equidistant=False).trajectory

    md_initial = tdata['water_depth']
    md_final = survey[-1]['md']

    well = set_well(tdata, survey, operation)

    time = []
    rop_steps = []
    depths = sorted([x[2] for x in well.casings])
    if operation == 'drilling':

        prev_point = md_initial

        cummulative_time = []

        for x in range(len(depths)):
            distance = depths[x] - prev_point
            time_section = distance / well.rop_list[x]
            time.append(time_section)
            cummulative_time.append(sum(time))
            prev_point = depths[x]
        time.append((md_final - prev_point) / well.rop_list[-1])
        cummulative_time.append(sum(time))
        depths = list(depths) + [md_final]
        if depths[0] == 0:
            depths = depths[1:]
            time = time[1:]
            cummulative_time = cummulative_time[1:]

        tcirc = sum(time) * 3600  # drilling time, s
        for x in cummulative_time:
            rop_steps.append(round(x * 3600 / tcirc / time_steps))
    else:
        tcirc = tdata['time'] * 3600    # circulating time, s

    time_step = tcirc / time_steps  # seconds per time step

    log_temp_values(well, initial=True)     # log initial temperature distribution
    well.delta_time = time_step
    time_n = time_step
    well.op = operation

    td = len(well.trajectory)-1

    for x in range(time_steps):

        if well.op == 'drilling':
            d = depths[0]
            rop = well.rop_list[0]
            t = time[0] * 3600
            for y in range(len(time)):
                if time_n < sum(time[:y+1])*3600:
                    d = depths[y]
                    if len(well.rop_list) > 1:
                        rop = well.rop_list[y]
                    t = sum(time[:y+1])*3600
                    break

            bit_depth = d - rop/3600 * (t - time_n)
            bit_position = [cell for cell, point in enumerate(well.trajectory) if point['md'] <= bit_depth][-1]
            td = bit_position

        if time_steps > 1:

            if td > 0:
                well = calc_temperature_distribution(well, time_step, td)
                well = define_temperatures(well, td)

                log_temp_values(well, time_n)

                if well.op == 'drilling':
                    if x in range(len(rop_steps)):
                        well.temperatures['in_pipe'] = well.temp_fm
                        well.temperatures['pipe'] = well.temp_fm
                        well.temperatures['annulus'] = well.temp_fm
                        well.temperatures['casing'] = well.temp_fm
                        well.temperatures['riser'] = well.temp_fm
                        well.temperatures['sr'] = well.temp_fm
                        for i in well.sections:
                            for j in range(len(well.trajectory)):
                                i[j]['temp'] = well.temp_fm[j]
                                i[j]['temp_fm'] = well.temp_fm[j]

            well.time = time_n / 3600

        time_n += time_step

    if smooth:
        smooth_results(well)

    additional_points(well)

    return well


def define_temperatures(well, bit_position):
    """
    Make the temperature values more reachable since they are is a dictionary along the entire well. Once this function
    takes place, the temperatures will be available as lists.
    :return: a dictionary with lists of temperature values and also a list with respective depth points.
    """

    temp_in_pipe = [x['temp'] for x in well.sections[0][:bit_position+1]] + \
                   [None] * (len(well.trajectory) - (bit_position + 1))
    temp_pipe = [x['temp'] for x in well.sections[1][:bit_position+1]] + \
                [None] * (len(well.trajectory) - (bit_position + 1))
    temp_annulus = [x['temp'] for x in well.sections[2][:bit_position+1]] + \
                   [None] * (len(well.trajectory) - (bit_position + 1))
    temp_casing = []
    temp_riser = []
    temp_sr = [x['temp'] for x in well.sections[4]]
    for y, x in enumerate(well.md):

        if well.riser_cells > 0 and x < well.water_depth:
            temp_casing.append(None)
            temp_riser.append(well.sections[3][y]['temp'])
        else:
            temp_riser.append(None)
            if x <= well.casings[0, 2]:
                temp_casing.append(well.sections[3][y]['temp'])
            else:
                temp_casing.append(None)

    well.temperatures = {'md': list(well.md),
                         'formation': well.temp_fm,
                         'in_pipe': temp_in_pipe,
                         'pipe': temp_pipe,
                         'annulus': temp_annulus,
                         'casing': temp_casing,
                         'riser': temp_riser,
                         'sr': temp_sr}

    return well


def log_temp_values(well, time=0.0, initial=False):
    time = round(time/3600, 2)
    if initial:
        well.temp_log = [{'time': time,
                          'in_pipe': well.temp_fm,
                          'pipe': well.temp_fm,
                          'annulus': well.temp_fm,
                          'casing': well.temp_fm,
                          'riser': well.temp_fm,
                          'sr': well.temp_fm}]
    else:
        well.temp_log.append(
            {'time': time,
             'in_pipe': [x['temp'] for x in well.sections[0]],
             'pipe': [x['temp'] for x in well.sections[1]],
             'annulus': well.temperatures['annulus'],
             'casing': well.temperatures['casing'],
             'riser': well.temperatures['riser'],
             'sr': well.temperatures['sr']}
        )


def temperature_behavior(well):
    """
    Function to simulate the temperature behavior.

    Arguments:
        well (obj): well temperature distribution object

    Returns:
        temperature behavior object
    """

    time = []
    temp_bottom = []
    temp_outlet = []
    temp_max = []
    temp_fm = []

    for x in well.temp_log[1:]:
        cells = len(well.md) - x['annulus'].count(None)
        time.append(x['time'])
        temp_bottom.append(x['in_pipe'][cells-1])
        temp_outlet.append(x['annulus'][0])
        temp_max.append(max(x['annulus'][:cells-1]))
        temp_fm.append(well.temp_fm[cells-1])

    temp_bottom = list(scipy.signal.savgol_filter(temp_bottom, 59, 3))
    temp_max = list(scipy.signal.savgol_filter(temp_max, 59, 3))
    temp_outlet = list(scipy.signal.savgol_filter(temp_outlet, 59, 3))
    temp_fm = list(scipy.signal.savgol_filter(temp_fm, 59, 3))

    class TempBehavior(object):
        def __init__(self):
            self.time = time
            self.bottom = temp_bottom
            self.outlet = temp_outlet
            self.max = temp_max
            self.formation_td = temp_fm

        def plot(self, title=True):
            fig = plot_behavior(self, title)

            return fig

    return TempBehavior()


def smooth_results(well):

    well.temperatures['in_pipe'] = list(scipy.signal.savgol_filter(well.temperatures['in_pipe'], 15, 3))
    well.temperatures['annulus'] = list(scipy.signal.savgol_filter(well.temperatures['annulus'], 15, 2))

    cells = len(well.md) - np.count_nonzero(np.isnan(well.temperatures['annulus']))
    ref = int(0.9 * cells - well.time*0.2)
    t_bottom = np.mean(well.temperatures['annulus'][ref:])

    x_new = well.md[ref:]

    # Smooth annulus
    interp_ann = make_interp_spline([well.md[ref - 1], well.md[ref], well.md[-1]],
                                    [well.temperatures['annulus'][ref - 1], well.temperatures['annulus'][ref],
                                     t_bottom],
                                    k=2)
    temp_annulus = interp_ann(x_new)

    # Smooth in_pipe
    interp_in_pipe = make_interp_spline(well.md[:ref-2] + [well.md[-1]],
                                        well.temperatures['in_pipe'][:ref-2] + [t_bottom],
                                        k=2)
    temp_in_pipe = interp_in_pipe(x_new)

    well.temperatures['in_pipe'] = well.temperatures['in_pipe'][:ref] + list(temp_in_pipe)
    well.temperatures['annulus'] = well.temperatures['annulus'][:ref] + list(temp_annulus)


def additional_points(well):
    if well.water_depth > 0:
        depths = [point['md'] for point in well.trajectory]
        seabed_point = False
        for idx, md in enumerate(depths):
            if idx > 0:
                if md > well.water_depth and not seabed_point:
                    well.temperatures['md'].insert(idx, well.water_depth)

                    well.temperatures['formation'].insert(idx,
                                                          np.interp(well.water_depth, [depths[idx - 1], md],
                                                                    [well.temperatures['formation'][idx - 1],
                                                                     well.temperatures['formation'][idx]]))
                    well.temperatures['in_pipe'].insert(idx,
                                                        np.interp(well.water_depth, [depths[idx - 1], md],
                                                                  [well.temperatures['in_pipe'][idx - 1],
                                                                   well.temperatures['in_pipe'][idx]]))
                    well.temperatures['pipe'].insert(idx,
                                                     np.interp(well.water_depth, [depths[idx - 1], md],
                                                               [well.temperatures['pipe'][idx - 1],
                                                                well.temperatures['pipe'][idx]]))
                    well.temperatures['annulus'].insert(idx,
                                                        np.interp(well.water_depth, [depths[idx - 1], md],
                                                                  [well.temperatures['annulus'][idx - 1],
                                                                   well.temperatures['annulus'][idx]]))
                    well.temperatures['riser'].insert(idx, well.temperatures['riser'][idx - 1])
                    well.temperatures['casing'].insert(idx, well.temperatures['casing'][idx])
                    well.temperatures['sr'].insert(idx,
                                                   np.interp(well.water_depth, [depths[idx - 1], md],
                                                             [well.temperatures['sr'][idx - 1],
                                                              well.temperatures['sr'][idx]]))
                    seabed_point = True

                reference = well.casings[0][2]
                if md > reference != 0:
                    well.temperatures['md'].insert(idx + 1, reference)

                    well.temperatures['formation'].insert(idx + 1,
                                                          np.interp(reference, [depths[idx - 1], md],
                                                                    [well.temperatures['formation'][idx],
                                                                     well.temperatures['formation'][idx + 1]]))
                    well.temperatures['in_pipe'].insert(idx + 1,
                                                        np.interp(reference, [depths[idx - 1], md],
                                                                  [well.temperatures['in_pipe'][idx],
                                                                   well.temperatures['in_pipe'][idx + 1]]))
                    well.temperatures['pipe'].insert(idx + 1,
                                                     np.interp(reference, [depths[idx - 1], md],
                                                               [well.temperatures['pipe'][idx],
                                                                well.temperatures['pipe'][idx + 1]]))
                    well.temperatures['annulus'].insert(idx + 1,
                                                        np.interp(reference, [depths[idx - 1], md],
                                                                  [well.temperatures['annulus'][idx],
                                                                   well.temperatures['annulus'][idx + 1]]))
                    well.temperatures['riser'].insert(idx + 1, None)
                    well.temperatures['casing'].insert(idx + 1, well.temperatures['casing'][idx])
                    well.temperatures['sr'].insert(idx,
                                                   np.interp(reference, [depths[idx - 1], md],
                                                             [well.temperatures['sr'][idx],
                                                              well.temperatures['sr'][idx + 1]]))
                    break
