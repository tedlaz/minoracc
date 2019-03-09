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