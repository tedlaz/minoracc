from named_tuples import TransDetail
from named_tuples import TransHeader
from named_tuples import DetailPerigraphi
from utils import iso_dat
from utils import dec
from logger import logger


def parse_imerologio(fil, enc='WINDOWS-1253'):
    # Create list with lines to exclude
    EXC = (' ' * 150 + 'Σελίδα',
           ' ' * 33 + 'ΓΕΝΙΚΟ ΗΜΕΡΟΛΟΓΙΟ',
           '  Ημ/νία      Α/Α ΚΒΣ Στοιχεία Αρθρου',
           '  Ημ/νία     Α/Α ΚΒΣ  Στοιχεία Αρθρου',
           '                      Σχετ. Παραστατ.',
           '  -----------------------------------',
           ' ' * 38 + 'Από μεταφορά',
           ' ' * 123 + '-------------- --------------',
           ' ' * 70 + 'Σύνολα Σελίδας',
           ' ' * 70 + 'Σε Μεταφορά',
           ' ' * 70 + 'Σύνολα Περιόδου',
           ' ' * 152
           )
    dat = par = lmo = lmp = xre = pis = pe2 = per = ''
    tno = lno = 0
    SDAT = slice(2, 12)  # Ημερομηνία
    SPAR = slice(22, 48)  # Παραστατικό
    SLMO = slice(48, 60)  # Κωδικός λογαριασμού
    SLMP = slice(77, 122)  # Ονομασία λογαριασμού
    SXRE = slice(124, 137)  # Χρέωση
    SPIS = slice(139, 152)  # Πίστωση
    SPE2 = slice(22, 48)  # Έξτρα περιγραφή
    SPER = slice(48, -1)  # Περιγραφή
    dper = {}
    dlmo = {}
    trah = {}
    trad = {}
    arthro = {}
    unparsed_lines = {}
    with open(fil, encoding=enc) as ofil:
        for i, lin in enumerate(ofil):
            llin = len(lin)  # Το υπολογίζω εδώ μία φορά
            if llin < 48:  # Δεν έχουν νόημα γραμμές μικρότερες του 48
                continue
            elif lin.startswith(EXC):  # Exclude lines
                continue
            elif lin[50] == '.' and lin[53] == '.' and lin[134] == ',':
                if lin[4] == '/' and lin[7] == '/':
                    tno += 1
                    dat = iso_dat(lin[SDAT])
                    par = lin[SPAR].strip()
                    trah[tno] = TransHeader(dat, par)
                lno += 1
                lmo = lin[SLMO].strip()
                lmp = lin[SLMP].strip()
                xre = dec(lin[SXRE].strip().replace('.', '').replace(',', '.'))
                pis = dec(lin[SPIS].strip().replace('.', '').replace(',', '.'))
                if lmo in dlmo:
                    if dlmo[lmo] != lmp:
                        logger.error('Διαφορά στο όνομα %s:  %s -> %s' % (
                               lmo, dlmo[lmo],lmp))
                else:
                    dlmo[lmo] = lmp
                trad[lno] = TransDetail(tno, lmo, xre, pis)
                arthro[tno] = arthro.get(tno, [])
                arthro[tno].append(lno)
            elif llin < 132:  # Πρόκειται για γραμμή περιγραφής
                pe2 = lin[SPE2].strip()
                per = lin[SPER].strip()
                dper[tno] = DetailPerigraphi(per, pe2)
            else:
                unparsed_lines[i] = lin
    if len(unparsed_lines) > 0:
        logger.error('parse_imerologio unparsed lines : %s' % unparsed_lines)
    else:
        logger.info('parse_imerologio parsed everynthing ok !!!')
    return {'tr_header': trah, 'tr_lines': trad, 'tr_per': dper,
            'lmoi': dlmo, 'arthra': arthro, 'errors': unparsed_lines}


def final(filename):
    results = parse_imerologio(filename)
    transactions = []
    for trid, header in results['tr_header'].items():
        tran = {'id': trid,
                'date': header.date, 
                'par': header.parastatiko, 
                'per': results['tr_per'][trid].perigrafi,
                'pe2': results['tr_per'][trid].lineperigrafi,
                'afm': ''
                }
        tran['lines'] = []
        tdebit = tcredit = 0
        for idd in results['arthra'][trid]:
            tdebit += results['tr_lines'][idd].debit
            tcredit += results['tr_lines'][idd].credit
            typ = 0
            val = 0
            if results['tr_lines'][idd].debit == 0:
                typ = 2
                val = results['tr_lines'][idd].credit
            elif results['tr_lines'][idd].credit == 0:
                typ = 1
                val = results['tr_lines'][idd].debit
            if typ == 0:
                raise ValueError("Either debit or credit")
            tran['lines'].append({
                'code': results['tr_lines'][idd].account_code,
                'typ': typ,
                'val': val})
        if tdebit != tcredit:
            raise ValueError("Transaction is not balanced")
        transactions.append(tran)
    return transactions, results['lmoi']


def transaction_type(trans, rules):
    account_list = []
    acclist = set([l['code'] for l in trans['lines']])
    dclist = [l['typ'] for l in trans['lines']]
    lis = {i['code']: i['typ'] for i in trans['lines']}
    # print(acclist)
    # print(dclist)
    for rule in rules:
        rule_mach = True
        for key in rule['acc']:
            match = False
            for code in lis:
                if code.startswith(key) and lis[code] == rule['acc'][key]:
                    match = True
                    break
            if not match:
                rule_mach = False
                break
        if rule_mach:
            print(lis, rule['acc'], rule['name'])
            return True
    print(lis, "? ? ? ? ? ? ? ? ? ? ")
    return False


if __name__ == '__main__':
    filename = "/home/ted/Documents/pelates/samaras/2019b/el2019b.txt"
    # results = parse_imerologio(filename)
    # print(results['tr_header'])
    ruls = [{'name': 'Ejoda xrisis me fpa', 'acc': {'64': 1, '54.00': 1, '53.98': 2}},
            {'name': 'Ejoda xrisis me fpa', 'acc': {'62': 1, '54.00': 1, '53.98': 2}},
            {'name': 'Ejoda xrisis xoris fpa metrita', 'acc': {'64': 1, '38.0': 2}},
            {'name': 'Agores a ylon me fpa', 'acc': {'24': 1, '54.00': 1, '50': 2}},
            {'name': 'Agores a ylon ejoterikoy', 'acc': {'24': 1, '50.01': 2}},
            {'name': 'Agores a analosimon me fpa', 'acc': {'25': 1, '54.00': 1, '50': 2}},
            {'name': 'Poliseis proionton me fpa', 'acc': {'71': 2, '54.00': 2, '30': 1}},
            {'name': 'Poliseis proionton xoris fpa', 'acc': {'71': 2, '30': 1}},
            {'name': 'Poliseis Ypiresion me fpa', 'acc': {'73': 2, '54.00': 2, '30': 1}},
            {'name': 'Ejoda xrisis ', 'acc': {'64': 1, '53.98': 2}},
            {'name': 'Eispraji apo Pelath', 'acc': {'38': 1, '30': 2}},
            {'name': 'Epitages apo Pelath', 'acc': {'33.90': 1, '30': 2}},
            {'name': 'Epitages pelaton se promithefti', 'acc': {'33.90': 2, '50': 1}},
            {'name': 'Pliromi Promithefti', 'acc': {'38': 2, '50': 1}},
            {'name': 'Pliromi Promithefti', 'acc': {'38': 2, '53': 1}},
            {'name': 'Pliromi Foron', 'acc': {'38': 2, '54': 1}},
            {'name': 'Pliromi EFKA', 'acc': {'38': 2, '55.01': 1}},
            {'name': 'Pliromi IKA ergazomenon', 'acc': {'38': 2, '55.00': 1}},
            {'name': 'Epistrofi metrita Promithefti', 'acc': {'38': 1, '53': 2}},
            {'name': 'Analipsi metrita', 'acc': {'38.03': 2, '38.00': 1}},
            {'name': 'Katathesi metrita', 'acc': {'38.03': 1, '38.00': 2}},
            {'name': 'Metafora se daneiako', 'acc': {'38.03': 2, '52.00': 1}},
            {'name': 'Metafora ', 'acc': {'38.03': 2, '38.03.00': 1}},
            {'name': 'Trapezika ejoda', 'acc': {'38.03': 2, '65': 1}},
            {'name': 'Tokoi', 'acc': {'52.00': 2, '65': 1}},
            {'name': 'Misthodosia', 'acc': {'60': 1, '55': 2, '53': 2}}, 
            ]
    for tran in final(filename)[0][0:950]:
        transaction_type(tran, ruls)
