import unittest
import transaction_book as bk
import transaction as ts


class Tests(unittest.TestCase):

    def test_001(self):
        tlb = bk.TransactionBook()
        tr1 = ts.Transaction('2019-01-03', 'ΤΔΑ3', 'Δοκιμαστικό 3', '123123123')
        tr1.add_line('64.07.00.000', 1, 10)
        tr1.add_line('54.00.06.624', 1, 2.4)
        tr1.add_line('38.03.00.000', 2, 12.4)
        tlb.add(tr1)
        tr2 = ts.Transaction('2019-01-02', 'ΤΔΑ2', 'Δοκιμαστικό 2', '111222333')
        tr2.add_line('70.00.01.000', 2, 100)
        tr2.add_line('54.00.07.724', 2, 24)
        tr2.add_line('38.00.00.000', 1, 124)
        tlb.add(tr2)
        tr2 = ts.Transaction('2019-01-04', 'ΤΔΑ4', 'Δοκιμαστικό 4', '111222333')
        tr2.add_line('71.00.00.000', 2, 100)
        tr2.add_line('54.00.07.724', 2, 24)
        tr2.add_line('38.00.00.000', 1, 124)
        tlb.add(tr2)
        # print(tlb.get(1))
        # tlb.journal_print()
        # tlb.kartella_print('38', '2018-01-01', '2019-12-31')
        # tlb.balance_sheet_print()
        tlb.myf()
        print(tlb.synal)
