"""Help function to split digits to thousants (123456 becomes 123.456)

    :param txt: text to split
    :param separator: The separator to use

    :return: txt separated by separator in group of three

    Example::

        >>> import gr
        >>> gr.triades('abcdefg')
        'a.bcd.efg'
        >>> gr.triades('abcdefg', separator='|')
        'a|bcd|efg'
"""
from operator import attrgetter
from collections import namedtuple
from collections import defaultdict
import transaction as ts
from named_tuples import KartellaLine
from named_tuples import MyfLine
from utils import dec
from config import MYFEX
from logger import logger


class TransactionBook:
    """Το βιβλίο λογιστικών εγγραφών"""

    def __init__(self, name=None):
        self.name = name
        self.transactions = []
        self.synal = set()

    @property
    def size(self):
        return len(self.transactions)

    def add(self, transaction):
        """Add transaction to book"""
        self.transactions.append(transaction)
        if transaction.afm != '':
            self.synal.add(transaction.afm)

    def get(self, transaction_number):
        """Get a specific arthro"""
        if transaction_number > self.size:
            logger.info(f"Trans number {transaction_number} > {self.size}")
            transaction_number = self.size
        if transaction_number < 1:
            logger.info(f"Trans number {transaction_number} < 1")
            transaction_number = 1
        return self.transactions[transaction_number - 1]

    def get_print(self, transaction_number):
        """Get a specific arthro"""
        print(self.get(transaction_number))

    def balance_sheet(self, date_from=None, date_to=None):
        """Return balance sheet for a given period
        :param date_from: Date from or Null
        :param deta_to: Date to or Null

        :return: Isozygio

        Example::

            >>> book.balance_sheet('2018-01-01', '2018-12-31')
            ....
        """
        bsh = defaultdict(lambda: {'debit': 0, 'credit': 0})
        for trans in sorted(self.transactions, key=attrgetter('date')):
            if date_from:
                 if not (date_from <= trans.date):
                     continue
            if date_to:
                if not (trans.date <= date_to):
                    continue
            for lin in trans.lines:
                for acc in lin.account.hierarchy:
                    bsh[acc]['debit'] += lin.debit
                    bsh[acc]['credit'] += lin.credit
        return bsh

    def balance_sheet_print(self, date_from=None, date_to=None):
        stt = "%-20s %12s %12s %12s"
        bsh = self.balance_sheet(date_from, date_to)
        print('')
        print(stt % ("Λογαριασμός", 'Χρέωση', 'Πίστωση', 'Υπόλοιπο'))
        for acc in sorted(bsh.keys()):
            cre = bsh[acc]['debit']
            deb = bsh[acc]['credit']
            ypo = cre - deb
            print(stt % (acc, cre, deb, ypo))

    def journal(self, date_from=None, date_to=None):
        """Return journal of transactions sorted by date for a given period"""
        jour = []
        for trans in sorted(self.transactions, key=attrgetter('date')):
            if date_from:
                 if not (date_from <= trans.date):
                     continue
            if date_to:
                if not (trans.date <= date_to):
                    continue
            jour.append(trans)
        return jour

    def journal_print(self, date_from=None, date_to=None):
        journal = self.journal(date_from, date_to)
        print('')
        for transaction in journal:
            print(transaction)

    def kartella(self, account, date_from=None, date_to=None):
        """Return kartella for account and given period"""
        karl = []
        rest = 0
        for trans in sorted(self.transactions, key=attrgetter('date')):
            if date_from:
                 if not (date_from <= trans.date):
                     continue
            if date_to:
                if not (trans.date <= date_to):
                    continue
            for lin in trans.lines:
                # Get every child account
                if lin.account.code.startswith(account):
                    rest += lin.rest
                    nt = KartellaLine(trans.date, lin.account.code,
                                      trans.parastatiko, trans.perigrafi,
                                      lin.debit, lin.credit, rest)
                    karl.append(nt)
        return karl

    def kartella_print(self, account, date_from=None, date_to=None):
        kart = self.kartella(account, date_from, date_to)
        print('')
        print("Καρτέλλα λογαριασμού %s" % account)
        if date_from:
            print("Από : %s" % date_from)
        if date_to:
            print("Έως : %s" % date_to)
        for l in kart:
            stt = '%s %s %-12s %-40s %12s %12s %12s'
            print(stt %(l.date, l.acc, l.par[:12], l.per[:40], l.debit, l.credit, l.rest))
        print('')

    def book_ee(self, date_from, date_to):
        """Return book of revenues/expenses for a given period"""
        pass

    def vat_calculate(self, date_from, date_to):
        """Calculate vat for given period"""
        pass

    def myf(self):
        cval = defaultdict(dict)
        cfpa = defaultdict(dict)
        myfl = []
        for tran in self.transactions:
            myf = tran.myf
            if myf:
                # cval[myf.category][myf.decr] = cval[myf.category].get(myf.decr, 0) + myf.amount
                # cfpa[myf.category][myf.decr] = cfpa[myf.category].get(myf.decr, 0) + myf.tax
                if myf.category == 'PRO-VAT':
                    cat = 'PRO'
                    if myf.tax == 0:
                        amn = dec(myf.amount / dec(1.24))
                        tax = myf.amount - amn
                        # print(tran.date, tran.parastatiko, tran.perigrafi, tran.afm, amn, tax)
                    else:
                        amn = myf.amount
                        tax = myf.tax
                    myfl.append(MyfLine(myf.date, myf.afm, cat, myf.decr, amn, tax))
                elif myf.category == 'PEL-LIA':
                    myfl.append(MyfLine(myf.date, '', myf.category, myf.decr, myf.amount, myf.tax))
                elif myf.category == 'PRO' and myf.afm in MYFEX:
                    print(tran)
                    myfl.append(MyfLine(myf.date, '', 'PRO-CUB', myf.decr, myf.amount, myf.tax))
                else:
                    myfl.append(myf)
        # print(cval, cfpa)
        return myfl

    def myf_totals(self, year):
        myflines = self.myf()
        aapo, aeos = '%s-01-01' % year, '%s-03-31' % year
        bapo, beos = '%s-04-01' % year, '%s-06-30' % year
        capo, ceos = '%s-07-01' % year, '%s-09-30' % year
        dapo, deos = '%s-10-01' % year, '%s-12-31' % year
        fnl = {}
        per = 0
        for lin in myflines:
            if aapo <= lin.date <= aeos:
                per = 1
            elif bapo <= lin.date <= beos:
                per = 2
            elif capo <= lin.date <= ceos:
                per = 3
            elif dapo <= lin.date <= deos:
                per = 4
            else:
                print('Error')
            fnl[per] = fnl.get(per, {})
            fnl[per][lin.category] = fnl[per].get(lin.category, {})
            fnl[per][lin.category][lin.afm] = fnl[per][lin.category].get(lin.afm, {})
            fnl[per][lin.category][lin.afm][lin.decr] = fnl[per][lin.category][lin.afm].get(lin.decr, [0, 0, 0])
            fnl[per][lin.category][lin.afm][lin.decr][0] += lin.amount
            fnl[per][lin.category][lin.afm][lin.decr][1] += lin.tax
            fnl[per][lin.category][lin.afm][lin.decr][2] += 1
        return fnl
