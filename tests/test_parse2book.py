import unittest
import parse2book as p2b


class Tests(unittest.TestCase):
     def test_001(self):
         fil = "/home/ted/tmp/fpa/el201812.txt"
         p2b.parse2book(fil)