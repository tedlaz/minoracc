from collections import namedtuple
import transaction_line as trl
import utils as utl
import config as cfg
from named_tuples import MyfLine
from named_tuples import EeLine
from named_tuples import TransTotalVals
from enums import Decr
from logger import logger


class Transaction:
    def __init__(self, date, parastatiko, perigrafi, per2='', afm=''):
        """Create a new Transaction"""
        self.date = date
        self.parastatiko = parastatiko
        self.perigrafi = perigrafi
        self.per2 = per2
        self.afm = afm
        self.lines = []

    def add_line(self, account, ttype, value, comment='', accname=''):
        """Insert a new transactionLine"""
        new_line = trl.TransactionLine(account, ttype, value, comment, accname)
        self.lines.append(new_line)

    def add_line_dc(self, account, debit, credit, comnt='', acc_name=''):
        """Insert a new transaction line from debit credit values"""
        delta = debit - credit
        nli = trl.TransactionLine(
                    account, Decr.DEBIT.value, delta, comnt, acc_name)
        self.lines.append(nli)

    def add_line_final(self, account, comment=''):
        """Insert final TransactionLine"""
        diff = self.total_delta
        if diff < 0:
            self.lines.append(trl.TransactionLine(account, cfg.DEBIT, -diff, comment))
        elif diff > 0:
            self.lines.append(trl.TransactionLine(account, cfg.CREDIT, diff, comment))

    def __str__(self):
        sta = '\nDate: %s, par: %s, per: %s per2: %s\n' % (self.date, self.parastatiko, self.perigrafi, self.per2)
        for lin in self.lines:
            sta += '%s\n' % lin.__str__()
        return sta

    @property
    def to_ee(self):
        """Create esoda - ejoda line
            else return Null
        """
        # NT_EE = nt('NT_EE', "date typ par per poso vat")
        if self.is_apotelesma:
            poso = vat = 0
            for line in self.lines:
                if line.is_vat:
                    vat += line.value_delta
                elif line.is_apotelesma:
                    poso += line.value_delta
            if poso < 0:
                poso = -poso
                vat = -vat
                typp = 2
            else:
                typp = 1
            if vat < 0:
                raise ValueError
            rva = EeLine(self.date, typp, self.parastatiko, self.perigrafi,
                          poso, vat)
            return rva

    @property
    def normal_or_debit(self):
        """Is transaction normal, debit or mixed"""
        seta = set()
        for line in self.lines:
            if line.line_type:
                seta.add(line.line_type)
        if len(seta) == 0:
            return None
        elif len(seta) == 1:
            return list(seta)[0]
        else:
            return 'mixed'

    @property
    def line_types(self):
        typoi = set()
        for line in self.lines:
            typoi.add(line.account_type)
        return typoi

    @property
    def is_vat(self):
        """Returns True if
           1.transaction contains VAT
           2.transaction contains APOTELESMA
        """
        seta = set()
        for lin in self.lines:
            if lin.is_vat:
                seta.add('VAT')
            elif lin.is_apotelesma:
                seta.add('APOTELESMA')
        return seta == {'VAT', 'APOTELESMA'}

    @property
    def number_of_lines(self):
        """Returns number of lines"""
        return len(self.lines)

    @property
    def is_binary(self):
        """Returns True if contains two and only two transaction lines"""
        return self.number_of_lines == 2

    @property
    def total_delta(self):
        return round(sum([lin.value_delta for lin in self.lines]), 2)

    @property
    def is_balanced(self):
        """Checks if transaction is balanced"""
        return (self.total_delta == 0) and (self.number_of_lines > 1)

    @property
    def is_apotelesma(self):
        """True εάν το άρθρο περιέχει γραμμή αποτελεσματική"""
        for lin in self.lines:
            if lin.is_apotelesma:
                return True
        return False

    @property
    def is_transfer(self):
        """True αν υπόρχουν <<Μόνο>> κινήσεις μεταφοράς"""
        for lin in self.lines:
            if lin.account.omada not in cfg.TRANSFTYP:
                return False
        return True

    @property
    def tags(self):
        tgs = set()
        if self.is_balanced:
            tgs.add('BALANCED')
        else:
            tgs.add('UNBALANCED')
        if self.is_apotelesma:
            tgs.add('APOTELESMA')
        if self.is_vat:
            tgs.add('VAT')
        if self.is_transfer:
            tgs.add('TRANSFER')
        if self.is_binary:
            tgs.add('BINARY')
        if self.normal_or_debit:
            tgs.add(self.normal_or_debit)
        return tgs

    def check_vat(self, threshold=0.01):
        apo = []
        vat = []
        if self.is_vat:
            for lin in self.lines:
                if lin.is_apotelesma:
                    apo.append(lin.value_delta)
                elif lin.is_vat:
                    vat.append(lin.value_delta)
            if utl.vat_best_mach(apo, vat, threshold):
                return True
            else:
                logger.info("VAT Error in Transaction:\n%s" % self)
                return False
        return None

    @property
    def total_val_vat_old(self):
        """Επιστρέφει το συνολικό ποσό, το συνολικό ΦΠΑ και τον τύπο
           (normal, credit) της εγγραφής
        """
        totalvalue = totalvat = 0
        typoi = set()
        for line in self.lines:
            if line.line_type:
                typoi.add(line.line_type)
                totalvalue += line.value
            if line.is_vat:
                totalvat += line.value
        if len(typoi) == 1:  # Φυσιολογικά θα πρέπει να έχει μόνο μια τιμή
            return TransTotalVals(totalvalue, totalvat, list(typoi)[0])
        elif len(typoi) > 1:
            logger.error("Error: %s %s %s %s" %  (self, totalvalue,
                                                  totalvat, typoi))
            return None
        return None

    @property
    def total_val_vat(self):
        """Επιστρέφει το συνολικό ποσό, το συνολικό ΦΠΑ και τον τύπο
           (normal, credit) της εγγραφής
        """
        totalvalue_normal= totalvalue_credit = totalvat = 0
        typoi = set()
        for line in self.lines:
            if line.line_type:
                typoi.add(line.line_type)
            if line.line_type == 'normal':
                totalvalue_normal += line.value
            elif line.line_type == 'credit':
                totalvalue_credit += line.value
            if line.is_vat:
                totalvat += line.value
        if len(typoi) == 0:
            return None
        if totalvalue_normal >= totalvalue_credit:
            rest = totalvalue_normal - totalvalue_credit
            return TransTotalVals(rest, totalvat, 'normal')
        else:
            rest = totalvalue_credit - totalvalue_normal
            return TransTotalVals(rest, totalvat, 'credit')

    @property
    def myf(self):
        myf_tags = set()
        for lin in self.lines:
            if lin.account.myf:  # Αν βρεί μια τιμή είναι αρκετή και σταματάει
                myf_tags.add(lin.account.myf)
        tvs = self.total_val_vat
        if (len(myf_tags) == 1) and tvs:
            return MyfLine(self.date, self.afm, list(myf_tags)[0],
                           tvs.decr, tvs.amount, tvs.tax)
        elif len(myf_tags) > 1:
            logger.error("Error: %s %s" % (self, myf_tags))
            return None
        return None