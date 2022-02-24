import unittest
from rain import get_rain_data


class Tests(unittest.TestCase):
    def test_get_rain_data_default_file(self):
        rain_data = get_rain_data()
        self.assertEqual(len(rain_data), 1162584)
        self.assertEqual(len(rain_data[0]), 4)

    def test_get_rain_data_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, get_rain_data, '/home/eben/foo.csv')
