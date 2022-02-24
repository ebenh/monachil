import unittest
from rain import get_rain_data, get_lat_lon


class Tests(unittest.TestCase):
    def test_get_rain_data_default_file(self):
        rain_data = get_rain_data()
        self.assertEqual(len(rain_data), 1162584)
        self.assertEqual(len(rain_data[0]), 4)

    def test_get_rain_data_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, get_rain_data, '/home/eben/foo.csv')

    def test_get_lat_lon_valid_city(self):
        self.assertEqual(get_lat_lon('Toronto'), (43.6534817, -79.3839347))

    def test_get_lat_lon_case_sensitivity(self):
        self.assertEqual(get_lat_lon('tOrOnTo'), (43.6534817, -79.3839347))

    def test_get_lat_lon_whitespace(self):
        self.assertEqual(get_lat_lon(' Toronto  '), (43.6534817, -79.3839347))

    def test_get_lat_lon_invalid_city(self):
        self.assertRaises(ValueError, get_lat_lon, 'FooBazBar')
