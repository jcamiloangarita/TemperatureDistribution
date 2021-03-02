from unittest import TestCase
import well_profile as wp

trajectory = wp.load(r'https://github.com/pro-well-plan/pwptemp/raw/master/pwptemp/tests/trajectory1.xlsx',
                     equidistant=True)


class TestInitCond(TestCase):

    def test_init_cond_drilling(self):
        pass

    def test_init_cond_production(self):
        pass

    def test_init_cond_injection(self):
        pass
