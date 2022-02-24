import unittest
from rain import load_rain_data, get_lat_lon, filter_rainy_days


class Tests(unittest.TestCase):
    def test_get_rain_data_default_file(self):
        rain_data = load_rain_data()
        self.assertEqual(len(rain_data), 1162584)
        self.assertEqual(len(rain_data[0]), 4)

    def test_get_rain_data_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, load_rain_data, '/home/eben/foo.csv')

    def test_get_lat_lon_valid_city(self):
        self.assertEqual(get_lat_lon('Toronto'), (43.6534817, -79.3839347))

    def test_get_lat_lon_case_sensitivity(self):
        self.assertEqual(get_lat_lon('tOrOnTo'), (43.6534817, -79.3839347))

    def test_get_lat_lon_whitespace(self):
        self.assertEqual(get_lat_lon(' Toronto  '), (43.6534817, -79.3839347))

    def test_get_lat_lon_invalid_city(self):
        self.assertRaises(ValueError, get_lat_lon, 'FooBazBar')

    def test_filter_rainy_days_no_data(self):
        self.assertEqual(filter_rainy_days((32.7174202, -117.1627728), []), [])

    def test_filter_rainy_days(self):
        rain_data = load_rain_data()
        expected_data = [
            ('2021-10-16', '11.689456'),
            ('2021-10-16', '9.970568'),
            ('2021-10-21', '72.44653'),
            ('2021-10-21', '61.9733'),
            ('2021-10-21', '48.436115'),
            ('2021-10-21', '44.8336'),
            ('2021-11-06', '10.885766'),
            ('2021-11-06', '9.332636')
        ]
        self.assertEqual(filter_rainy_days((37.3361905, -121.890583), rain_data), expected_data)

    def test_filter_rainy_days_dist_thresh_zero(self):
        rain_data = load_rain_data()
        self.assertEqual(filter_rainy_days((37.3361905, -121.890583), rain_data, dist_thresh=0), [])

    def test_filter_rainy_days_rain_thresh_infinity(self):
        import math
        rain_data = load_rain_data()
        self.assertEqual(filter_rainy_days((37.3361905, -121.890583), rain_data, rain_thresh=math.inf), [])
