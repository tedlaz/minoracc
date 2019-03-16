from utils import iso_dat
from utils import dec
from utils import is_afm
from named_tuples import Kin
from collections import defaultdict


def parse_esex(fil, enc='WINDOWS-1253'):
    # Create list with lines to exclude
    EXC = (' ' * 164 + 'Σελίδα',
           '   Κινήσεις ανά Ημέρα',
           '     A/A Τύπος Εγγραφής',
           '-------- ------------------------- ',
           '   Σύνολα ημέρας',
           ' ' * 92 + '-------------------- -------------------- ',
           ' ' * 53 + 'Σύνολα Εξόδων',
           ' ' * 53 + 'Σύνολα Εξόδων',
           '  Γενικά Σύνολα',
           ' ' * 53 + 'Εξόδων',
    )
    SDAT = slice(32, 42)  # Ημερομηνία
    SAA = slice(0, 8)  # Αριθμός άρθρου
    STYP = slice(9, 34)  # Τύπος
    SPAR = slice(35, 66)  # Παραστατικό
    SAFM = slice(67, 76)  # ΑΦΜ
    SLMO = slice(67, 91)  # όλο το πεδίο άν δεν υπάρχει ΑΦΜ
    SLMP = slice(77, 91)  # μόνο μετά το ΑΦΜ
    SVAL = slice(93, 112)  # Καθαρή αξία
    SFPA = slice(114, 133)  # ΦΠΑ
    STOT = slice(156, 175)  # Σύνολο
    dat = typ = par = per = afm =''
    aar = val = fpa = tot = 0
    # lines = []
    # lind = defaultdict(list)
    lind = defaultdict(dict)
    with open(fil, encoding=enc) as ofil:
        for lin in ofil:
            llin = len(lin)
            if llin < 40:
                continue
            elif lin.startswith(EXC):  # Exclude lines
                continue
            elif lin.startswith('  Κινήσεις της '):
                # print(lin)
                dat = iso_dat(lin[SDAT])
            elif lin[109] == ',' and lin[130] == ',' and lin[151]:
                aar = int(lin[SAA].strip())
                typ = lin[STYP].strip()
                par = lin[SPAR].strip()
                afm = lin[SAFM].strip()
                if is_afm(afm):
                    per = lin[SLMP].strip()
                else:
                    afm = ''
                    per = lin[SLMO].strip()
                val = dec(lin[SVAL].strip().replace('.', '').replace(',', '.'))
                fpa = dec(lin[SFPA].strip().replace('.', '').replace(',', '.'))
                tot = dec(lin[STOT].strip().replace('.', '').replace(',', '.'))
                "id dat typ par per afm val fpa tot"
                kin = Kin(aar, dat, typ, par, per, afm, val, fpa, tot)
                if afm != '':
                    # lines.append(kin)
                    lind[dat][kin.par] = kin.afm
    return lind


if __name__ == '__main__':
    fil = "/home/ted/tmp/fpa/ee201812.txt"
    prs = parse_esex(fil)
    # print('\n'.join(["%s : %s " % (i.par, i.afm) for i in prs['2018-01-04']]))
    # print(len(prs))
    for dat, kinl in prs.items():
        for kin, afm in kinl.items():
            print('%s %-15s %s' % (dat, kin, afm))
