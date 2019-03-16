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
                        logger.error('> Διαφορά στο όνομα %s:  %s -> %s' % (
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
        logger.error('> parse_imerologio unparsed lines : %s' % unparsed_lines)
    else:
        logger.info('> parse_imerologio parsed everynthing ok !!!')
    return {'tr_header': trah, 'tr_lines': trad, 'tr_per': dper,
            'lmoi': dlmo, 'arthra': arthro, 'errors': unparsed_lines}
