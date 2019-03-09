from collections import namedtuple
import transaction_line as trl
import utils as utl
import config as cfg


# VATPOSN = [24, 13, 6]
# VATPOSS = [17, 9, 4]
NT_EE = namedtuple('NT_EE', "date typ par per poso vat")


class Transaction:
    def __init__(self, date, parastatiko, perigrafi, lines=None):
        """Create a new Transaction"""
        self.date = date
        self.parastatiko = parastatiko
        self.perigrafi = perigrafi
        self.lines = []

    def add_line(self, account, ttype, value, comment=''):
        """Insert a new transactionLine"""
        new_line = trl.TransactionLine(account, ttype, value, comment)
        self.lines.append(new_line)

    def add_line_final(self, account, comment=''):
        """Insert final TransactionLine"""
        diff = self.total_delta
        if diff < 0:
            self.lines.append(trl.TransactionLine(account, cfg.DEBIT, -diff, comment))
        elif diff > 0:
            self.lines.append(trl.TransactionLine(account, cfg.CREDIT, diff, comment))

    def __str__(self):
        sta = '\nDate: %s, par: %s, per: %s\n' % (self.date, self.parastatiko, self.perigrafi)
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
            rva = NT_EE(self.date, typp, self.parastatiko, self.perigrafi,
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
                print('\nVAT Error in Transaction:', self)
                return False
        return None
