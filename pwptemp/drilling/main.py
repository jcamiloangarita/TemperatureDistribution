def temp_time(n, well, log=False):
    """
    Function to calculate the well temperature distribution during drilling at a certain circulation time n.
    :param n: circulation time, hours
    :param well: a well object created from the function set_well()
    :param log: save distributions between initial time and circulation time n (each 1 hour)
    :return: a temperature distribution object
    """
    from .initcond import init_cond
    from .heatcoefficients import heat_coef
    from .linearsystem import temp_calc
    from .plot import profile
    from math import log
    # Simulation main parameters
    time = n  # circulating time, h
    tcirc = time * 3600  # circulating time, s
    deltat = 60
    tstep = int(tcirc / deltat)
    ic = init_cond(well)
    well = well.define_density(ic, cond=0)

    hc = heat_coef(well, deltat)
    temp = temp_calc(well, ic, hc)
    temp_log = []

    for x in range(1, tstep):
        well = well.define_density(ic, cond=1)
        ic.tdsio = temp.tdsi
        ic.tdso = temp.tds
        ic.tao = temp.ta
        ic.tcsgo = temp.t3
        ic.tsr = temp.tsr
        hc_new = heat_coef(well, deltat)
        temp = temp_calc(well, ic, hc_new)

        if log:
            temp_log.append(temp)

    class TempDist(object):
        def __init__(self):
            self.tdsi = temp.tdsi
            self.tds = temp.tds
            self.ta = temp.ta
            self.tr = temp.tr
            self.tcsg = temp.tcsg
            self.toh = temp.toh
            self.tsr = temp.tsr
            self.tfm = ic.tfm
            self.time = time
            self.md = well.md
            self.riser = well.riser
            self.csgs_reach = temp.csgs_reach
            self.deltat = deltat
            if log:
                self.temp_log = temp_log[::60]

        def plot(self, sr=False):
            profile(self, sr)

        def well(self):
            return well

        def behavior(self):
            stab = temp_behavior(self)
            return stab

    return TempDist()


def temp_behavior(temp_dist):

    ta = [x.ta for x in temp_dist.temp_log]

    tbot = []
    tout = []

    for n in range(len(ta)):
        tbot.append(ta[n][-1])
        tout.append(ta[n][0])

    class Behavior(object):
        def __init__(self):
            self.finaltime = temp_dist.time
            self.tbot = tbot
            self.tout = tout
            self.tfm = temp_dist.tfm

        def plot(self):
            from .plot import behavior
            behavior(self)

    return Behavior()


def temp_times(n, x, well):
    from numpy import arange
    from .plot import profile_multitime
    temps_list = []
    times_list = []
    for i in list(arange(x, n+x, x)):
        current_temp = temp_time(i, well)
        temps_list.append(current_temp)
        times_list.append(i)

    class TempDist(object):
        def __init__(self):
            self.values = temps_list
            self.times = times_list

        def plot(self, tdsi=True, ta=False, tr=False, tcsg=False, tfm=True, tsr=False):
            profile_multitime(self, tdsi=tdsi, ta=ta, tr=tr, tcsg=tcsg, tfm=tfm, tsr=tsr)

    return TempDist()


# BUILDING GENERAL FUNCTIONS FOR DRILLING MODULE


def temp(n, mdt=3000, casings=[], wellpath_data=[], d_openhole=0.216, grid_length=50, profile='V', build_angle=1, kop=0,
         eob=0, sod=0, eod=0, kop2=0, eob2=0, change_input={}, log=False):
    """
    Main function to calculate the well temperature distribution during drilling operation. This function allows to
    set the wellpath and different parameters involved.
    :param n: circulation time, hours
    :param mdt: measured depth of target, m
    :param casings: list of dictionaries with casings characteristics (od, id and depth)
    :param wellpath_data: load own wellpath as a list
    :param d_openhole: diameter of open hole section, m
    :param grid_length: number of cells through depth
    :param profile: type of well to generate. Vertical ('V'), S-type ('S'), J-type ('J') and Horizontal ('H1' or 'H2')
    :param build_angle: build angle, °
    :param kop: kick-off point, m
    :param eob: end of build, m
    :param sod: start of drop, m
    :param eod: end of drop, m
    :param kop2: kick-off point 2, m
    :param eob2: end of build 2, m
    :param change_input: dictionary with parameters to set.
    :param log: save distributions between initial time and circulation time n (each 1 hour)
    :return: a well temperature distribution object
    """
    from .input import data, set_well
    from .. import wellpath
    tdata = data(casings, d_openhole)
    for x in change_input:   # changing default values
        if x in tdata:
            tdata[x] = change_input[x]
        else:
            raise TypeError('%s is not a parameter' % x)
    if len(wellpath_data) == 0:
        depths = wellpath.get(mdt, grid_length, profile, build_angle, kop, eob, sod, eod, kop2, eob2)
    else:
        depths = wellpath.load(wellpath_data, grid_length)
    well = set_well(tdata, depths)
    temp_distribution = temp_time(n, well, log)

    return temp_distribution


def temps(n, x, mdt=3000, casings=[], wellpath_data=[], bit=0.216, grid_length=50, profile='V', build_angle=1, kop=0,
          eob=0, sod=0, eod=0, kop2=0, eob2=0, change_input={}):
    from .input import data, set_well
    from .. import wellpath
    tdata = data(casings, bit)
    for i in change_input:   # changing default values
        if i in tdata:
            tdata[i] = change_input[i]
        else:
            raise TypeError('%s is not a parameter' % i)
    if len(wellpath_data) == 0:
        depths = wellpath.get(mdt, grid_length, profile, build_angle, kop, eob, sod, eod, kop2, eob2)
    else:
        depths = wellpath.load(wellpath_data, grid_length)
    well = set_well(tdata, depths)
    temp_distributions = temp_times(n, x, well)

    return temp_distributions


def input_info(about='all'):
    from .input import info
    info(about)
