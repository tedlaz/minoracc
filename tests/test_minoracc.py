import unittest
import minoracc as mac


class Tests(unittest.TestCase):
    def test_a1(self):
        self.assertEqual(mac.stg('1213,23'), '1213.23')

    def test_a2(self):
        self.assertEqual(mac.stg('1213.23'), '1213.23')
