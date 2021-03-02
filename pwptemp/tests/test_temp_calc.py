from unittest import TestCase
import well_profile as wp

trajectory = wp.load(r'https://github.com/pro-well-plan/pwptemp/raw/master/pwptemp/tests/trajectory1.xlsx',
                     equidistant=True)


class TestLinearSystem(TestCase):

    def test_temp_calc_production(self):
        pass

    def test_temp_calc_injection(self):
        pass
