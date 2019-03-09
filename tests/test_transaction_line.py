import unittest
import transaction_line as ts


class Tests(unittest.TestCase):

    def test_001(self):
        tl = ts.TransactionLine('70.00.024', 1, 30)
        self.assertEqual(tl.value_delta, 30)

    def test_002(self):
        tl = ts.TransactionLine('70.00.024', 2, 30)
        self.assertEqual(tl.value_delta, -30)

    def test_003(self):
        tl = ts.TransactionLine('70.00.024', 2, -20)
        self.assertEqual(tl.line_type, 'credit')

    def test_004(self):
        tl = ts.TransactionLine('70.00.024', 1, 20)
        self.assertEqual(tl.line_type, 'credit')

    def test_005(self):
        tl = ts.TransactionLine('64.00.024', 1, 20)
        self.assertEqual(tl.line_type, 'normal')

    def test_006(self):
        tl = ts.TransactionLine('64.00.024', 2, -20)
        self.assertEqual(tl.line_type, 'normal')

    def test_007(self):
        with self.assertRaises(Exception):
            ts.TransactionLine('64.00.024', 3, -20)

    def test_008(self):
        tl = ts.TransactionLine('64.00.024', 1, -20)
        self.assertEqual(tl.account_type, "LINE-EKSODA")

    def test_009(self):
        tl = ts.TransactionLine('54.00.024', 2, 20)
        self.assertEqual(tl.account_type, "LINE-FPA")

    def test_010(self):
        tl = ts.TransactionLine('64.00.024', 2, 20)
        self.assertEqual(tl.is_apotelesma, True)

    def test_011(self):
        tl = ts.TransactionLine('54.00.024', 2, 20)
        self.assertEqual(tl.is_apotelesma, False)

    def test_012(self):
        tl = ts.TransactionLine('70.00.024', 2, 20)
        self.assertEqual(tl.is_apotelesma, True)