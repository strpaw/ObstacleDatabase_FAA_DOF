import unittest
from obstacle_faa_dof_db.dof_utils.dof_coordinates import *
from obstacle_faa_dof_db.dof_utils.dof_conversion_errors import LongitudeConversionError, LatitudeConversionError


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

    def test_dmsh_to_dd_longitude_valid(self):
        longitudes = [
            ('180 00 00E', 180),
            ('180 00 00.0E', 180),
            ('045 30 00.000E', 45.5),
            ('000 30 00.000W', -0.5)
        ]

        for lon_dmsh, lon_dd in longitudes:
            self.assertAlmostEqual(lon_dd, dmsh_to_dd(lon_dmsh, "LONGITUDE"))

    def test_dmsh_to_dd_longitude_invalid(self):
        longitudes = [
            ('180 00 00N', 180),
            ('180 00 00.0S', 180),
            ('045 30 00.000S', 45.5),
            ('000 30 00.000N', -0.5)
        ]

        for lon_dmsh, lon_dd in longitudes:
            self.assertIsNone(dmsh_to_dd(lon_dmsh, "LONGITUDE"))

    def test_dmsh_to_dd_latitude_valid(self):
        latitudes = [
            ('90 00 00N', 90),
            ('90 00 00.0S', -90),
            ('45 30 00.000S', -45.5),
            ('00 30 00.000N', 0.5),
        ]

        for lat_dmsh, lat_dd in latitudes:
            self.assertAlmostEqual(lat_dd, dmsh_to_dd(lat_dmsh, "LATITUDE"))

    def test_dmsh_to_dd_latitude_invalid(self):
        latitudes = [
            '180 00 00E',
            '180 00 00.0W',
            '045 30 00.000E',
            '000 30 00.000E'
        ]

        for lat_dmsh in latitudes:
            self.assertIsNone(dmsh_to_dd(lat_dmsh, "LATITUDE"))

    def test_longitude_to_dms_valid(self):
        longitudes = [
            ('180 00 00E', 180),
            ('180 00 00.0E', 180),
            ('045 30 00.000E', 45.5),
            ('000 30 00.000W', -0.5)
        ]

        for lon_dmsh, lon_dd in longitudes:
            self.assertAlmostEqual(lon_dd, longitude_to_dms(lon_dmsh))

    def test_longitude_to_dms_invalid(self):
        longitudes = [
            '180 00 00N',
            '180 00 00.0S',
            '045 30 00.000S',
            '000 30 00.000N',
        ]

        for lon_dmsh in longitudes:
            self.assertRaises(LongitudeConversionError, longitude_to_dms, lon_dmsh)

    def test_latitude_to_dms_valid(self):
        latitudes = [
            ('90 00 00N', 90),
            ('90 00 00.0S', -90),
            ('45 30 00.000S', -45.5),
            ('00 30 00.000N', 0.5),
        ]

        for lat_dmsh, lat_dd in latitudes:
            self.assertAlmostEqual(lat_dd, latitude_to_dms(lat_dmsh))

    def test_latitude_to_dms_invalid(self):
        latitudes = [
            '180 00 00E',
            '180 00 00.0W',
            '045 30 00.000E',
            '000 30 00.000E'
        ]

        for lat_dmsh in latitudes:
            self.assertRaises(LatitudeConversionError, latitude_to_dms, lat_dmsh)
