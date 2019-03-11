from enum import Enum


class Decr(Enum):
    """Debit or credit"""
    DEBIT = 1
    CREDIT = 2


class Myft(Enum):
    """Myf types"""
    CUSTOMER = 3
    CUSTOMER_NO_NAME = 4
    VENDOR = 5
    VENDOR_NO_NAME = 6


class Acct(Enum):
    """Account type (CEDITED, DEBITED, MIXED)"""
    DEBITED = 1
    CREDITED = 2
    MIXED = 3


class Omades(Enum):
    TAKSEOS = 0
    PAGIA = 1
    APOTHEMATA = 2
    APAITISEIS = 3
    KEFALAIO = 4
    YPOXREOSEIS = 5
    EKSODA = 6
    ESODA = 7
    APOTELESMATA = 8
    ANALYTIKI = 9
