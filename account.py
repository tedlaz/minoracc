import config as cfg
import enums
from logger import logger


class Account:
    def __init__(self, code, name=None):
        self.code = code
        if name:
            self.name = name
        else:
            self.name = code

    @property
    def omada(self):
        """Normally the first digit if code is numeric"""
        if self.code[0] in cfg.OMADES:
            return self.code[0]
        else:
            # Εάν δεν είναι αριθμός τότε θα πρέπει να βρεθεί αντιστοίχιση
            return self.code.split(cfg.SPLITTER)[0]

    @property
    def hierarchy(self):
        """if account is 'ab.cd.ef.ghi'
           returns ('a', 'ab', 'ab.cd', 'ab.cd.ef', 'ab.cd.ef.ghi')
        """
        spl = self.code.split(cfg.SPLITTER)
        ranks = [cfg.SPLITTER.join(spl[:i + 1]) for i in range(len(spl))]
        if self.omada == ranks[0]:
            return tuple(ranks)
        return tuple(['9', self.omada] + ranks)

    @property
    def dc_type(self):
        """Account type normal status
            DEBITABLE, CREDITABLE, MIXED
        """
        return cfg.TEAM.get(self.omada, cfg.MIX)

    @property
    def is_vat(self):
        """True if account=vat else False"""
        return self.code.startswith(cfg.VATACC)

    @property
    def is_apot(self):
        """Εάν είναι λογαριασμός αποτελεσμάτων"""
        return self.omada in cfg.APOTELTYP

    @property
    def is_ee(self):
        """Εάν είναι λογαριασμός εσόδων-εξόδων"""
        return (self.omada in cfg.EETYP) or self.is_vat

    @property
    def tags(self):
        """Account tags for multiple uses"""
        logger.info(f'from inside tags {self}')
        tgs = {self.omada, cfg.DEBCREDMIX[self.dc_type]}
        if self.is_apot:
            tgs.add('APOTELESMA')
        else:
            tgs.add('TRANSFER')
        if self.is_vat:
            tgs.add('VAT')
        if self.is_ee:
            tgs.add('EE')
        return tgs

    @property
    def myf(self):
        """Returns myf tag"""
        for key in cfg.MYF.keys():
            if self.code.startswith(key):
                return cfg.MYF[key]
        return None

    def __str__(self):
        return f'{self.code} {self.name}'
