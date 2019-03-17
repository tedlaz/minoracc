import unittest
import transaction as ts
from utils import dec
from named_tuples import MyfLine
from enums import MyfCat


class Tests(unittest.TestCase):

    def test_301(self):
        tr = ts.Transaction('2018-01-01', 'tda1', 'test')
        tr.add_line('20.01.2024', 1, 100)
        tr.add_line('54.00.2024', 1, 24)
        tr.add_line('50.00.1223', 2, 124)
        self.assertEqual(tr.normal_or_debit, 'normal')

    def test_302(self):
        tr2 = ts.Transaction('2019-01-01', 'tda1', 'test')
        tr2.add_line('20.01.2024', 1, -10)
        tr2.add_line('54.00.2024', 1, -2.4)
        tr2.add_line('50.00.1223', 2, -12.4)
        self.assertEqual(tr2.normal_or_debit, 'credit')

    def test_303(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('20.01.2024', 1, -10)
        tr2.add_line('54.00.2024', 1, -2.4)
        tr2.add_line('20.02.2024', 1, 10)
        tr2.add_line('54.00.2124', 1, 2.4)
        self.assertEqual(tr2.normal_or_debit, 'mixed')

    def test_304(self):
        tr = ts.Transaction('2018-01-01', 'tda1', 'test')
        tr.add_line('20.01.2024', 1, 100)
        tr.add_line('54.00.2024', 1, 24)
        self.assertEqual(tr.is_balanced, False)
        tr.add_line('50.00.1223', 2, 124)
        self.assertEqual(tr.is_balanced, True)

    def test_305(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('20.01.2024', 1, -10)
        tr2.add_line('54.00.2024', 1, -2.4)
        tr2.add_line('20.02.2024', 1, 10)
        tr2.add_line('54.00.2124', 1, 2.4)
        self.assertEqual(tr2.line_types, {'LINE-APOTHEMATA', 'LINE-FPA'})

    def test_306(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('20.01.2024', 1, -10)
        tr2.add_line('54.00.2024', 1, -2.4)
        tr2.add_line('20.02.2024', 1, 10)
        tr2.add_line('54.00.2124', 1, 2.4)
        self.assertEqual(tr2.is_vat, True)

    def test_307(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('20.01.2024', 1, 10)
        tr2.add_line('20.02.2024', 2, 10)
        self.assertEqual(tr2.is_vat, False)

    def test_308(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('38.00.00', 1, 10)
        tr2.add_line('58.03.00', 2, 10)
        self.assertEqual(tr2.tags, {'BALANCED', 'BINARY', 'TRANSFER'})

    def test_309(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('20.01.2024', 1, -10)
        tr2.add_line('54.00.2024', 1, -2.4)
        tr2.add_line('20.02.2024', 1, 10)
        tr2.add_line('54.00.2124', 1, 2.4)
        self.assertEqual(tr2.tags, {'VAT', 'APOTELESMA', 'BALANCED', 'mixed'})

    def test_310(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('64.08.00', 1, 10)
        tr2.add_line('38.00.00', 2, 10)
        self.assertEqual(tr2.tags, {'BALANCED', 'BINARY', 'APOTELESMA', 'normal'})

    def test_311(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('64.08.00', 1, 10)
        tr2.add_line('54.00.24', 1, 2.4)
        tr2.add_line('38.00.00', 2, 12.4)
        # print(tr2.tags)
        # print(tr2.to_ee)

    def test_312(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('70.01.24', 2, 100)
        tr2.add_line('54.00.724', 2, 24)
        tr2.add_line('38.00.00', 1, 124)
        # print(tr2.tags)
        # print(tr2.to_ee)

    def test_313(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('70.01.24', 2, 100)
        tr2.add_line('54.00.724', 2, 24)
        tr2.add_line('38.00.00', 1, 124)
        self.assertEqual(tr2.check_vat(), True)

    def test_314(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('70.00.01.24', 2, 100)
        tr2.add_line('38.00.00', 1, 100)
        self.assertEqual(tr2.check_vat(), None)

    def test_315(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('70.01.24', 2, 105)
        tr2.add_line('54.00.724', 2, 24)
        tr2.add_line('38.00.00', 1, 129)
        self.assertEqual(tr2.check_vat(1.2), True)

    def test_316(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('70.01.24', 2, 105)
        tr2.add_line('54.00.724', 2, 24)
        tr2.add_line('38.00.00', 1, 129)
        self.assertEqual(tr2.check_vat(), False)

    def test_317(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('70.01.24', 2, 1000)
        tr2.add_line('54.00.724', 2, 240)
        tr2.add_line('70.01.13', 2, 1000)
        tr2.add_line('54.00.713', 2, 130)
        tr2.add_line('38.00.00', 1, 2370)
        self.assertEqual(tr2.check_vat(), True)

    def test_318(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('70.00.01.024', 2, 1000)
        tr2.add_line('54.00.724', 2, 240)
        tr2.add_line('70.00.01.013', 2, 1000)
        tr2.add_line('54.00.713', 2, 130)
        tr2.add_line('38.00.00', 1, 2370)
        tvl = MyfLine('2019-01-01', '', MyfCat.PEL, 'normal', 2000, 370)
        self.assertEqual(tr2.myf, tvl)

    def test_319(self):
        tr2 = ts.Transaction('2019-01-01', 'tda2', 'test again')
        tr2.add_line('70.00.00.024', 1, 1000)
        tr2.add_line('54.00.724', 1, 240)
        tr2.add_line('70.00.00.013', 1, 1000)
        tr2.add_line('54.00.713', 1, 130)
        tr2.add_line('38.00.00', 2, 2370)
        tvl = MyfLine('2019-01-01', '', MyfCat.PELLIA, 'credit', 2000, 370)
        self.assertEqual(tr2.myf, tvl)
