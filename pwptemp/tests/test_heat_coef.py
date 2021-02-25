from unittest import TestCase
import well_profile as wp

trajectory = wp.load(r'https://github.com/pro-well-plan/pwptemp/raw/master/pwptemp/tests/trajectory1.xlsx',
                     equidistant=True).trajectory


class TestHC(TestCase):
    def test_heat_coef_drilling(self):
        from pwptemp import well_system, inputs, heat_coefficients
        well = well_system.set_well(inputs.inputs_dict(), trajectory, 'drilling')
        well.op = 'drilling'
        bit_pos = 1
        heat_coefficients.add_heat_coefficients(well, 600, bit_pos)
        hc = well.sections
        self.assertTrue('comp_N/S' and 'comp_E' and 'comp_HeatSource' and 'comp_time' in hc[0][0])  # Inside Pipe
        self.assertTrue('comp_N/S' and 'comp_E' and 'comp_W' and 'comp_time' in hc[1][0])  # Pipe Wall
        self.assertTrue('comp_N/S' and 'comp_E' and 'comp_W' and 'comp_time' and 'comp_HeatSource' in hc[2][0])
        # Annulus
        self.assertTrue('comp_N/S' and 'comp_E' and 'comp_W' and 'comp_time' in hc[3][0])  # First Casing
        self.assertTrue('comp_N/S' and 'comp_E' and 'comp_W' and 'comp_time' in hc[4][0])  # Surrounding space

    def test_heat_coef_production(self):
        pass

    def test_heat_coef_injection(self):
        pass
