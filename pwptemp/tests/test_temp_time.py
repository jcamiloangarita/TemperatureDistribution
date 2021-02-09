from unittest import TestCase
import well_profile as wp

trajectory = wp.load(r'https://github.com/pro-well-plan/pwptemp/raw/master/pwptemp/tests/trajectory1.xlsx',
                     equidistant=True)


class TestMain(TestCase):

    def test_temp_time_injection(self):
        from pwptemp.injection import input, main
        tdata = input.data()
        well = input.set_well(tdata, trajectory)
        td = main.temp_time(2, well)
        self.assertEqual(len(td.tft), len(td.ta), len(td.tr))
        self.assertEqual(len(td.tc), len(td.tsr), len(td.tfm))
        self.assertEqual(td.time, 2)
        self.assertIsInstance(td.tft, list)
        self.assertIsInstance(td.ta, list)
        self.assertIsInstance(td.tr, list)
        self.assertIsInstance(td.tc, list)
        self.assertIsInstance(td.tsr, list)
        self.assertIsInstance(td.tfm, list)

    def test_temp_time_production(self):
        from pwptemp.production import input, main
        tdata = input.data()
        well = input.set_well(tdata, trajectory)
        td = main.temp_time(2, well)
        self.assertEqual(len(td.tft), len(td.ta), len(td.tr))
        self.assertEqual(len(td.tc), len(td.tsr), len(td.tfm))
        self.assertEqual(td.time, 2)
        self.assertIsInstance(td.tft, list)
        self.assertIsInstance(td.ta, list)
        self.assertIsInstance(td.tr, list)
        self.assertIsInstance(td.tc, list)
        self.assertIsInstance(td.tsr, list)
        self.assertIsInstance(td.tfm, list)