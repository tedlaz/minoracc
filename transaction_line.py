"""Transaction line"""
import config as cfg
import account as acc


class TransactionLine:
    stt = "Acc:%20s com:%30s deb:%12s cred:%12s"

    def __init__(self, account_code, ttype, value, comment=''):
        """Create a new TransactionLine
        :param account: The account code
        :param ttype: DEBIT(1), or CREDIT(2)
        :param value: Decimal nonzero number
        :param comment: Small comment about the line
        """
        assert ttype in (cfg.DEBIT, cfg.CREDIT)  # Only DEBIT or CREDIT
        assert value != 0  # Must have a nonzero value
        self.account = acc.Account(account_code)
        self.ttype = ttype
        self.value = value
        self.comment = comment
        self.normalize()

    @property
    def debit(self):
        if self.ttype == cfg.DEBIT:
            return self.value
        else:
            return 0

    @property
    def credit(self):
        if self.ttype == cfg.CREDIT:
            return self.value
        else:
            return 0

    @property
    def rest(self):
        if self.ttype == cfg.DEBIT:
            return self.value
        elif self.ttype == cfg.CREDIT:
            return -self.value
        else:
            return 0

    @property
    def value_delta(self):
        if self.ttype == cfg.DEBIT:
            return self.value
        elif self.ttype == cfg.CREDIT:
            return -self.value
        else:
            return 0

    def normalize(self):
        """Normalize transaction line
        """
        if self.value < 0:
            self.value = -self.value
            if self.ttype == cfg.DEBIT:
                self.ttype = cfg.CREDIT
            elif self.ttype == cfg.CREDIT:
                self.ttype = cfg.DEBIT

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
        if self.account.dc_type ==  self.ttype:
            return "normal"
        else:
            return "credit"

    def __str__(self):
        if self.ttype == cfg.DEBIT:
            debit = self.value
            credit = 0
        elif self.ttype == cfg.CREDIT:
            debit = 0
            credit = self.value
        else:
            debit = credit = self.value
        return self.stt % (self.account.code, self.comment, debit, credit)
