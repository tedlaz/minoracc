import unittest
import account as acc


class Tests(unittest.TestCase):

    def test_001(self):
        ac1 = acc.Account('54.00.2024', "ΦΠΑ αγορών 24%")
        print(ac1.hierarchy, ac1.tags)

    def test_002(self):
        ac1 = acc.Account('70.00.2024', "")
        print(ac1.hierarchy, ac1.tags)
