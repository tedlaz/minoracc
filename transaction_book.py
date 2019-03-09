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

KartellaLine = namedtuple('KartellaLine', "date acc par per debit credit rest")


class TransactionBook:

    def __init__(self):
        self.transactions = []

    @property
    def size(self):
        return len(self.transactions)

    def add(self, transaction):
        """Add transaction to book"""
        self.transactions.append(transaction)

    def get(self, transaction_number):
        """Get a specific arthro"""
        assert 0 < transaction_number < self.size
        return self.transactions[transaction_number - 1]

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
        print("Καρτέλλα λογαριασμού %s" % account)
        if date_from:
            print("Από : %s" % date_from)
        if date_to:
            print("Έως : %s" % date_to)
        for l in kart:
            stt = '%s %s %-10s %-20s %12s %12s %12s'
            print(stt %(l.date, l.acc, l.par, l.per, l.debit, l.credit, l.rest))
        print('')

    def book_ee(self, date_from, date_to):
        """Return book of revenues/expenses for a given period"""
        pass

    def vat_calculate(self, date_from, date_to):
        """Calculate vat for given period"""
        pass
