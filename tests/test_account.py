import unittest
import account as acc


class Tests(unittest.TestCase):

    def test_001(self):
        ac1 = acc.Account('54.00.2024', "ΦΠΑ αγορών 24%")
        self.assertEqual(('5', '54', '54.00', '54.00.2024'), ac1.hierarchy)
        # print(ac1.hierarchy, ac1.tags)

    def test_002(self):
        ac1 = acc.Account('70.00.00.2024', "")
        # print(ac1.hierarchy, ac1.tags)
        self.assertEqual(ac1.myf, 'PEL-LIA')