from unittest import TestCase
import pwptemp.production as ptp
import pwptemp.injection as pti
import well_profile as wp

trajectory = wp.load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx',
                     equidistant=True)


class TestMain(TestCase):
    def test_temp_behavior(self):
        t = 2

        # For Production
        st = ptp.temp(trajectory, t, log=True).behavior()
        self.assertIsInstance(st.finaltime, type(t))
        self.assertIsInstance(st.tout, list)

        # For Injection
        st = pti.temp(trajectory, t, log=True).behavior()
        self.assertIsInstance(st.finaltime, type(t))
        self.assertIsInstance(st.tbot, list)
