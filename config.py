from enums import MyfCat
DEBIT, CREDIT = 1, 2  # for account lines
DEBCRED = {1: 'DEBIT', 2: 'CREDIT'}  # reverse dictonary
DEB, CRED, MIX = 1, 2, 3  # For account normal state : Debit, credit, mix
DEBCREDMIX = {1: 'DEBITABLE', 2: 'CREDITABLE', 3: 'MIXED'}

SPLITTER = '.'
OMADES = '0123456789'  # Ομάδες λογαριασμών
ASSETSTYP = '1'  # Ομάδες Παγίων στοιχείων
APOTELTYP = '267'  # Ομάδες αποτελέσματος
TRANSFTYP = '35'  # Ομάδες μεταφοράς
EETYP = '1267'  # Ομάδες εσόδων-εξόδων
VATACC = "54.00."  # All vat accounts parent
TEAM = {'1': DEB, '2': DEB, '6': DEB, '7': CRED}
# TEAM = {'1': Acct.DEBITED,
#         '2': Acct.DEBITED,
#         '6': Acct.DEBITED,
#         '7': Acct.CREDITED}
ACCTYP = {'1': "LINE-PAGIA",
          '2': "LINE-APOTHEMATA",
          '3': "LINE-APAITHSEIS",
          '4': "LINE-KEFALAIO",
          '5': "LINE_YPOXREOSEIS",
          '6': "LINE-EKSODA",
          '7': "LINE-ESODA",
          '0': "LINE-TAKSEOS",
          '8': "LINE-APOTELESMATA",
          '9': "LINE-ANALYTIKH"}
VATPOSN = [24, 13, 6]  # Συντελεστές κανονικού ΦΠΑ
VATPOSS = [17, 9, 4]  # Συντελεστές μειωμένου ΦΠΑ
#         Vodaphone      ΔΕΗ         Cosmote        ΟΤΕ
MYFEX = ('094349850', '090000045', '094493766', '094019245')
MYF = {
    '14.03.': MyfCat.PRO,
    '20.01.': MyfCat.PRO,
    '24.01.': MyfCat.PRO,
    '25.01.': MyfCat.PRO,
    '61.00.': MyfCat.PRO,
    '62.': MyfCat.PRO,
    '64.00.': MyfCat.PROVAT,
    '64.02.': MyfCat.PRO,
    '64.07.': MyfCat.PRO,
    '64.98.': MyfCat.PRO,
    '70.00.00.': MyfCat.PELLIA,
    '70.00.01.': MyfCat.PEL,
    '71.00.00.': MyfCat.PELLIA,
    '71.00.01.': MyfCat.PEL,
    '73.00.00.': MyfCat.PELLIA,
    '73.00.01.': MyfCat.PEL}
