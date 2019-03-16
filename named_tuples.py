from collections import namedtuple


EeLine = namedtuple('EeLine', "date typ par per poso vat")
MyfLine = namedtuple('MyfLine', "date afm category decr amount tax")
TransTotalVals = namedtuple('TotalVals', "amount tax decr")

# for parser_el.py
TransDetail = namedtuple('TransDetail', 'tranid account_code debit credit')
TransHeader = namedtuple('TransHeader', 'date parastatiko')
DetailPerigraphi = namedtuple('DetailPerigraphi', 'perigrafi lineperigrafi')

# for parser_ee.py
Kin = namedtuple('Kin', "id dat typ par per afm val fpa tot")
# transaction_book.py
KartellaLine = namedtuple('KartellaLine', "date acc par per debit credit rest")
