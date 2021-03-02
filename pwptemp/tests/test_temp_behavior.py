from unittest import TestCase
import pwptemp.production as ptp
import pwptemp.injection as pti
import well_profile as wp

trajectory = wp.load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx',
                     equidistant=True).trajectory


class TestMain(TestCase):
    def test_temp_behavior(self):
        pass
