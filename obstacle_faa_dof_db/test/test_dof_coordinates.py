import unittest
from obstacle_faa_dof_db.dof_utils.dof_coordinates import *


class DofCoordinatesTest(unittest.TestCase):

    def test_check_hemisphere_valid_longitude(self):
        self.assertTrue(check_hemisphere("E", "LONGITUDE"))
        self.assertTrue(check_hemisphere("W", "LONGITUDE"))

    def test_check_hemisphere_invalid_longitude(self):
        self.assertFalse(check_hemisphere("N", "LONGITUDE"))

    def test_check_hemisphere_valid_latitude(self):
        self.assertTrue(check_hemisphere("S", "LATITUDE"))
        self.assertTrue(check_hemisphere("N", "LATITUDE"))

    def test_check_hemisphere_invalid_latitude(self):
        self.assertFalse(check_hemisphere("E", "LATITUDE"))

    def test_dmsh_to_dd_longitude_vaid(self):
        longitudes = [
            ('180 00 00E', 180),
            ('180 00 00.0E', 180),
            ('045 30 00.000E', 45.5),
            ('000 30 00.000W', -0.5)
        ]

        for lon_dmsh, lon_dd in longitudes:
            self.assertAlmostEqual(lon_dd, dmsh_to_dd(lon_dmsh, "LONGITUDE"))

    def test_dmsh_to_dd_longitude_vaid(self):
        longitudes = [
            ('180 00 00N', 180),
            ('180 00 00.0S', 180),
            ('045 30 00.000S', 45.5),
            ('000 30 00.000N', -0.5)
        ]

        for lon_dmsh, lon_dd in longitudes:
            self.assertIsNone(dmsh_to_dd(lon_dmsh, "LONGITUDE"))

    def test_dmsh_to_dd_latitude_vaid(self):
        latitudes = [
            ('90 00 00N', 90),
            ('90 00 00.0S', -90),
            ('45 30 00.000S', -45.5),
            ('00 30 00.000N', 0.5),
        ]

        for lat_dmsh, lat_dd in latitudes:
            self.assertAlmostEqual(lat_dd, dmsh_to_dd(lat_dmsh, "LATITUDE"))

    def test_dmsh_to_dd_latitude_vaid(self):
        latitudes = [
            '180 00 00E',
            '180 00 00.0W',
            '045 30 00.000E',
            '000 30 00.000E'
        ]

        for lat_dmsh in latitudes:
            self.assertIsNone(dmsh_to_dd(lat_dmsh, "LATITUDE"))
