import parser_el as elparse
from transaction_book import TransactionBook
from transaction import Transaction
from parser_ee import parse_esex
from parser_afm import parse_afm


def parse2book(elfile, dicee, dicafm, year):
    prs = elparse.parse_imerologio(elfile)
    book = TransactionBook("Test")
    print(book.name)
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
    # book.kartella_print("54.00.29")
    # book.get_print(25)
    # book.balance_sheet_print()
    # book.myf()
    ab1 = book.myf_totals(year)
    # print(ab1)
    for tr, typs in ab1.items():
        for typ, afms in typs.items():
            # print('%s->%s' % (tr, typ))
            for afm, decrs in afms.items():
                # print('%s->%s->%s' % (tr, typ, afm))
                for decr, vals in decrs.items():
                    print('%s->%7s->%9s->%s:%-5s: %12s %12s' % (tr, typ, afm, decr, vals[2], vals[0], vals[1]))
    # book.balance_sheet_print('2018-01-01', '2018-03-31')
    # book.balance_sheet_print()


if __name__ == '__main__':
    filee = "/home/ted/tmp/fpa/ee201812.txt"
    pee = parse_esex(filee)
    filafm = "/home/ted/tmp/totals/afm.txt"
    pafm = parse_afm(filafm)
    fil = "/home/ted/tmp/fpa/el201812.txt"
    parse2book(fil, pee, pafm, 2018)
