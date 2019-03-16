"""Transaction line"""
import config as cfg
import utils as utl
import account as acc
import enums


class TransactionLine:
    stt = "Acc:%20s com:%30s deb:%12s cred:%12s"

    def __init__(self, account_code, ttype, value, comment='', acc_name=None):
        """Create a new TransactionLine
        :param account: The account code
        :param ttype: DEBIT(1), or CREDIT(2)
        :param value: Decimal nonzero number
        :param comment: Small comment about the line
        """
        # assert ttype in (cfg.DEBIT, cfg.CREDIT)  # Only DEBIT or CREDIT
        # assert value != 0  # Must have a nonzero value
        self.account = acc.Account(account_code)
        self.ttype = enums.Decr(ttype)
        self.value = utl.dec(value)
        self.comment = comment
        self.normalize()

    @property
    def debit(self):
        if self.ttype == enums.Decr.DEBIT:
            return self.value
        else:
            return utl.dec(0)

    @property
    def credit(self):
        if self.ttype == enums.Decr.CREDIT:
            return self.value
        else:
            return utl.dec(0)

    @property
    def rest(self):
        if self.ttype == enums.Decr.DEBIT:
            return self.value
        elif self.ttype == enums.Decr.CREDIT:
            return -self.value
        else:
            return utl.dec(0)

    @property
    def value_delta(self):
        if self.ttype == enums.Decr.DEBIT:
            return self.value
        elif self.ttype == enums.Decr.CREDIT:
            return -self.value
        else:
            return utl.dec(0)

    def normalize(self):
        """Normalize transaction line
        """
        if self.value < 0:
            self.value = -self.value
            if self.ttype == enums.Decr.DEBIT:
                self.ttype = enums.Decr.CREDIT
            elif self.ttype == enums.Decr.CREDIT:
                self.ttype = enums.Decr.DEBIT

    @property
    def is_vat(self):
        """Checks if transaction line is vat account line"""
        return self.account.code.startswith(cfg.VATACC)

    @property
    def account_type(self):
        """Transaction line type"""
        if self.account.code.startswith(cfg.VATACC):
            return "LINE-FPA"
        elif self.account.omada in cfg.OMADES:
            return cfg.ACCTYP[self.account.omada]
        else:
            return "LINE-ERROR"

    @property
    def is_apotelesma(self):
        """Checks if line belongs to apotelesmata"""
        return self.account.is_apot

    @property
    def line_type(self):
        """Return Type of TransactionLine
           Depends on account, ttype and sign of value
           7, CREDIT, + = Esoda
           7, DEBIT, + = Esoda Pistotiko
           7, CREDIT, - = Esoda Pistotiko
           7, DEBIT, - = Esoda
        """
        if self.account.dc_type == cfg.MIX:
            return None
        if self.account.dc_type ==  self.ttype.value:
            return "normal"
        else:
            return "credit"

    def line_acc(self):
        stt = "%s-%s"
        return cfg.DEBCRED[self.ttype]

    def __str__(self):
        if self.ttype == enums.Decr.DEBIT:
            debit = self.value
            credit = utl.dec(0)
        elif self.ttype == enums.Decr.CREDIT:
            debit = utl.dec(0)
            credit = self.value
        else:
            debit = credit = self.value
        return self.stt % (self.account.code, self.comment, debit, credit)
