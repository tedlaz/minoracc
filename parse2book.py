import parser_el as elparse
from transaction_book import TransactionBook
from transaction import Transaction
from parser_ee import parse_esex
from parser_afm import parse_afm
from enums import MyfCat


def parse2book(elfile, eefile, afmfile, book_name="Test"):
    dicee = parse_esex(eefile)
    dicafm = parse_afm(afmfile)
    prs = elparse.parse_imerologio(elfile)
    book = TransactionBook(book_name)
    # Parse files and add transactions to book
    for trid, head in prs['tr_header'].items():
        per = prs['tr_per'][trid]
        trn = Transaction(head.date, head.parastatiko,
                          per.perigrafi, per.lineperigrafi)
        for eeper, eeafm in dicee[head.date].items():
            # print(eeper, eeafm, per.lineperigrafi)
            if eeper in per.lineperigrafi:
                trn.afm = eeafm
        for detail_line in prs['arthra'][trid]:
            dtl = prs['tr_lines'][detail_line]
            acn = prs['lmoi'][dtl.account_code]
            if dtl.account_code in dicafm.keys():
                trn.afm = dicafm[dtl.account_code]
            trn.add_line_dc(dtl.account_code, dtl.debit, dtl.credit, '', acn)
        book.add(trn)
    return book


def test(elfile, eefile, afmfile, year):
    bk1 = parse2book(elfile, eefile, afmfile)
    # book.kartella_print("54.00.29")
    # book.get_print(25)
    # book.balance_sheet_print()
    # book.myf()
    ab1 = bk1.myf_totals(year)
    for pr in sorted(ab1.keys()):
        typs = ab1[pr]
        ityps = [i.value for i in typs.keys()]
        for ityp in sorted(ityps):
            typ = MyfCat(ityp)
            afms = typs[typ]
            for afm in sorted(afms.keys()):
                decrs = afms[afm]
                for decr, vals in decrs.items():
                    print('%s->%13s->%9s->%s:%-5s: %12s %12s' % (pr, typ, afm, decr, vals[2], vals[0], vals[1]))
    # book.balance_sheet_print('2018-01-01', '2018-03-31')
    # bk1.balance_sheet_print()


if __name__ == '__main__':
    el_file = "/home/ted/tmp/fpa/el201812.txt"
    ee_file = "/home/ted/tmp/fpa/ee201812.txt"
    afm_file = "/home/ted/tmp/totals/afm.txt"
    test(el_file, ee_file, afm_file, 2018)
