import unittest
from rain import get_rain_data


class TestNumbers(unittest.TestCase):
    def test_get_rain_data_default_file(self):
        rain_data = get_rain_data()
        self.assertEqual(len(rain_data), 1162584)
        self.assertEqual(len(rain_data[0]), 4)

