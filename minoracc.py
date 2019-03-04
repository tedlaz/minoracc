#!/usr/bin/python3
import json
from textwrap import wrap
from operator import attrgetter
from collections import namedtuple
from collections import defaultdict
from collections import deque
LOGARIASMOS_SPLITTER = '.'
TRTUPLE = namedtuple('TRTUPLE', 'dat lmo per xr pi id')
STT = "%10s|%-30s|%-30s|%8s|%s\n"


def stg(num):
    num = str(num)
    spv = [num,]
    if '.' in num:
        spv = num.split('.')
    elif ',' in num:
        spv = num.split(',')
    assert len(spv) < 3
    if len(spv) == 1:
    	return spv[0] + '   '
    elif len(spv) == 2:
        if int(spv[1]) == 0:
            return spv[0] + '   '
    if len(spv[1]) == 1:
	    return spv[0] + '.' + spv[1] + ' '
    elif len(spv[1]) == 2:
	    return spv[0] + '.' + spv[1]
    else:
	    return spv[0] + '.' + spv[1][:2]


class Logariasmos:
    asset = 'πάγια'
    cash = 'ταμείο'
    income = 'εσοδα'
    expense = 'εξοδα'
    debitor = 'χρεώστες'
    creditor = 'πιστωτές'


def add_lists(lista, listb):
    fin = []
    assert len(lista) == len(listb)
    for i, _ in enumerate(lista):
        fin.append(lista[i] + listb[i])
    return fin


def ranks(lmos):
    als = lmos.split(LOGARIASMOS_SPLITTER)
    ranks = ['.'.join(als[:i + 1]) for i in range(len(als))]
    return ['𐅃 Σύνολα'] + ranks


class SimpleTransaction:
    __slots__ = ['dat', 'apo', 'se', 'val', 'per', 'id']

    def __init__(self, dat, apo, se, val, per, id):
        assert apo != se
        self.dat = dat
        self.apo = apo
        self.se = se
        self.val = val
        self.per = per
        self.id = id

    @property
    def linesd(self):
        return {self.se: {'xr': self.val, 'pi': 0, 'dat': self.dat, 'id': self.id},
                self.apo: {'xr': 0, 'pi': self.val, 'dat': self.dat, 'id': self.id}}

    @property
    def lines(self):
        return (TRTUPLE(dat=self.dat, lmo=self.se, xr=self.val, pi=0,
                        per=self.per, id=self.id),
                TRTUPLE(dat=self.dat, lmo=self.apo, xr=0, pi=self.val,
                        per=self.per, id=self.id))

    @property
    def row_line(self):
        return [self.dat, self.apo, self.se, self.val, self.per, self.id]

    @property
    def row_dict(self):
        return {'dat': self.dat, 'apo': self.apo, 'se': self.se,
                'val': self.val, 'per': self.per, 'id': self.id}

    @property
    def datgr(self):
        yyyy, mm, dd = self.dat.split('-')
        return dd + '/' + mm + '/' + yyyy

    @property
    def to_json(self):
        fdi = {'dat': self.dat, 'apo': self.apo, 'se': self.se,
               'val': self.val, 'per': self.per, 'id': self.id}
        return json.dumps(fdi, ensure_ascii=False)

    @property
    def to_json_normal(self):
        fdi = {'dat': self.dat, 'apo': self.apo, 'per': self.per, 'id': self.id,
               'lines': [{'lmo': self.apo, 'xr': 0, 'pi': self.val},
                         {'lmo': self.se, 'xr': self.val, 'pi': 0}]}
        return json.dumps(fdi, ensure_ascii=False)

    def __repr__(self):
        stt = 'SimpleTransaction(dat:%s, apo:%s, se:%s, val:%f, per:%s, id: %s)'
        return stt % (self.dat, self.apo, self.se, self.val, self.per, self.id)

    def __str__(self):
        stt = '%10s %-25s %-25s %10.2f %s %s'
        return stt % (self.dat, self.apo, self.se, self.val, self.per, self.id)


class Book:
    def __init__(self):
        self.trans = []
        self.lmoi = set()
        self.last_date = ''
        self.date_eos = None

    @classmethod
    def from_file(cls, filename, date_eos):
        fcls = cls()
        fcls.date_eos = date_eos
        fcls.read_file(filename)
        return fcls

    def to_model(self):
        headers = ('Ημ/νία', 'Από', 'Σε', 'Ποσό', 'Σχόλια', 'id')
        types = (0, 0, 0, 1, 0, 1)
        mdata = [tran.row_line for tran in self.trans]
        return {'headers': headers, 'types': types, 'mdata': mdata}

    def tail(self, last_lines=10):
        for trn in self.trans[last_lines*-1:]:
            print(trn)

    def create_and_add_transaction(self, dat, apo, se, val, per, id):
        """Add a new transaction"""
        tran = SimpleTransaction(dat, apo, se, val, per, id)
        self.add_transaction(tran)

    def add_transaction(self, simple_transaction):
        """Add an existing simple_transaction to Book"""
        assert isinstance(simple_transaction, SimpleTransaction)
        self.trans.append(simple_transaction)
        self.lmoi.add(simple_transaction.apo)
        self.lmoi.add(simple_transaction.se)

    def read_file(self, filename):
        # print('date_eos', self.date_eos)
        idx = 0 
        with open(filename, encoding="utf-8") as file:
            for i, line in enumerate(file.readlines()):
                if line.startswith('*'):
                    continue
                if len(line) < 20:
                    continue
                try:
                    dat, apo, se, val, per = (
                        j.strip() for j in line.strip().split('|'))
                    val = float(val.replace(',', '.'))
                except Exception:
                    print(i + 1, line)
                if self.date_eos:
                    if dat <= self.date_eos:
                        self.create_and_add_transaction(dat, apo, se, val, per,idx)
                        idx += 1
                else:
                    self.create_and_add_transaction(dat, apo, se, val, per, idx)
                    idx += 1
        self.last_date = dat

    def write_json_file(self, filename):
        data = '\n'.join([tr.to_json for tr in self.trans])
        return data

    def write_csv_files(self, filename, separate_lmoi=True):
        """We create two files:
        1. <filename>-lmoi.csv for accounts
        2.<filename>.csv for transactions
        """
        filename_lmoi = '%s-lmoi.csv' % filename
        filename_data = '%s.csv' % filename
        lmoi = list(sorted(self.lmoi))
        dlmoi = 'id|code\n'
        for i, lmo in enumerate(lmoi):
            no = str(i + 1)
            lin = '|'.join([no, lmo])
            dlmoi += lin + '\n'
        with open(filename_lmoi, 'w') as fil:
            fil.write(dlmoi)
        print('File %s created' % filename_lmoi)
        data = 'id|dat|apo|se|val|per\n'
        for i, trn in enumerate(self.trans):
            no = str(i + 1)
            idapo = str(lmoi.index(trn.apo) + 1)
            idse = str(lmoi.index(trn.se) + 1)
            val = str(trn.val)
            lin = '|'.join([no, trn.dat, idapo, idse, val, trn.per])
            data += lin + '\n'
        with open(filename_data, 'w') as fil:
            fil.write(data)
        print('File %s created' % filename_data)
        print('Finished creating csv files')

    def write_to_file(self, filename):
        # stt = "%10s|%-30s|%-30s|%8s|%s\n"
        data = ''
        for trn in self.trans:
            data += STT % (trn.dat, trn.apo, trn.se, stg(trn.val), trn.per)
        with open(filename, 'w') as fil:
            fil.write(data)
        print('Finished creating %s file' % filename)

    def isozygio(self):
        lmoi = defaultdict(lambda: {'xr': 0, 'pi': 0})
        for trn in self.trans:
            for line in trn.lines:
                for lmop in ranks(line.lmo):
                    lmoi[lmop]['xr'] += line.xr
                    lmoi[lmop]['pi'] += line.pi
        return lmoi

    def isozygio_model(self):
        lmoi = self.isozygio()
        headers = ("Λογαριασμοί", "Χρέωση", "Πίστωση", "Υπόλοιπο")
        align = (1, 3, 3, 3)
        typos = (0, 1, 1, 1)
        vals = []
        for lmo in sorted(lmoi.keys()):
            xr = round(lmoi[lmo]['xr'], 2)
            pi = round(lmoi[lmo]['pi'], 2)
            yp = round(xr - pi, 2)
            vals.append((lmo, xr, pi, yp))
        return headers, vals, align, typos

    def isozygio_kinoymenon(self):
        lmoi = defaultdict(lambda: {'xr': 0, 'pi': 0})
        for egr in self.trans:
            if egr.apo.startswith(('εξοδα', 'εσοδα')):
                lmoi['ανοιγμα']['pi'] += egr.val
            else:
                lmoi[egr.apo]['pi'] += egr.val
            if egr.se.startswith(('εξοδα', 'εσοδα')):
                lmoi['ανοιγμα']['xr'] += egr.val
            else:
                lmoi[egr.se]['xr'] += egr.val
        return lmoi

    def metafora_ypoloipon(self, dat, filename):
        # stt = "%10s|%-30s|%-30s|%8s|%s\n"
        lmoi = self.isozygio_kinoymenon()
        ant = 'ανοιγμα'
        per = 'Μεταφορά'
        lns = ''
        for lmo in sorted(lmoi.keys()):
            if lmo == ant:
                continue
            xr, pi = round(lmoi[lmo]['xr'], 2), round(lmoi[lmo]['pi'], 2)
            yp = round(xr - pi, 2)
            py = round(pi - xr, 2)
            if yp > 0:
                # lns += '|'.join((dat, ant, lmo, str(yp), per)) + '\n'
                lns += STT % (dat, ant, lmo, stg(yp), per)
            elif py > 0:
                # lns += '|'.join((dat, lmo, ant, str(py), per)) + '\n'
                lns += STT % (dat, lmo, ant, stg(py), per)
        with open(filename, 'w') as fil:
            fil.write(lns)

    def print_isozygio(self, not_show_zero_yp=False):
        stt = '%-50s %12.2f %12.2f %12.2f'
        lmoi = self.isozygio()
        print('\n      Ισοζύγιο λογαριασμών')
        for lmo in sorted(lmoi.keys()):
            xr, pi = round(lmoi[lmo]['xr'], 2), round(lmoi[lmo]['pi'], 2)
            yp = xr - pi
            if not_show_zero_yp and yp == 0:
                continue
            print(stt % (lmo, xr, pi, yp))
        print('')
        # print(stt % ('Σύνολα', tot['xr'], tot['pi'],tot['yp'] ))

    def print_all_kartelles(self):
        for lmo in sorted(self.lmoi):
            print(self._kartella(lmo))

    def _kartella(self, lmos):
        stt = '%10s %-50s %10.2f %10.2f %10.2f %s\n'
        stb = '%10s %-50s\n'
        stf = '\n%s\n' % lmos
        txr = tpi = ypo = 0
        anti = ''
        for tran in sorted(self.trans, key=attrgetter('dat')):
            if lmos == tran.apo:
                ypo = ypo - tran.val
                tpi += tran.val
                anti = tran.se
            elif lmos == tran.se:
                ypo = ypo + tran.val
                txr += tran.val
                anti = tran.apo
            else:
                continue
            per50 = wrap(tran.per, 50) if tran.per else ['']
            stf += stt % (tran.datgr, per50[0], 0, tran.val, ypo, anti)
            for per in per50[1:]:
                stf += stb % ('', per)
        # stf += stt % ('', '   Σύνολα', txr, tpi, ypo, '')
        return stf

    def kartella_model(self, lmos):
        headers = ('id', 'Ημ/νία', 'Περιγραφή', 'Χρέωση', 'Πίστωση', 'Υπόλοιπο')
        align = (1, 1, 1, 3, 3, 3)
        typos = (0, 0, 0, 1, 1, 1)
        vals = []
        ypo = 0
        for tr in sorted(self.trans, key=attrgetter('dat')):
            if tr.apo.startswith(lmos):
                ypo -= tr.val
                vals.append((tr.id, tr.datgr, tr.per, 0, tr.val, round(ypo, 2)))
            if tr.se.startswith(lmos):
                ypo += tr.val
                vals.append((tr.id, tr.datgr, tr.per, tr.val, 0, round(ypo, 2)))
        return headers, vals, align, typos
    
    def kartella(self, lmos):
        # if lmos in self.lmoi:
        #     return self._kartella(lmos)
        stt = '%10s %-50s %-35s %10.2f %10.2f %10.2f\n'
        stb = '%10s %-50s\n'
        stf = '\n%s\n' % lmos
        txr = tpi = ypo = 0
        for tr in sorted(self.trans, key=attrgetter('dat')):
            if tr.apo.startswith(lmos):
                ypo = ypo - tr.val
                tpi += tr.val
                per50 = wrap(tr.per, 50) if tr.per else ['']
                stf += stt % (tr.datgr, per50[0], tr.apo, 0, tr.val, ypo)
                for per in per50[1:]:
                    stf += stb % ('', per)
            if tr.se.startswith(lmos):
                ypo = ypo + tr.val
                txr += tr.val
                per50 = wrap(tr.per, 50) if tr.per else ['']
                stf += stt % (tr.datgr, per50[0], tr.se, tr.val, 0, ypo)
                for per in per50[1:]:
                    stf += stb % ('', per)
        # stf += stt % ('', '   Σύνολα', '', txr, tpi, ypo)
        return stf

    def kartella_joined(self, list_lmoi):
        stt = '%10s %-50s %-35s %10.2f %10.2f %10.2f\n'
        stb = '%10s %-50s\n'
        stf = '\n%s\n' % ','.join(list_lmoi)
        txr = tpi = ypo = 0
        for tr in sorted(self.trans, key=attrgetter('dat')):
            if tr.apo in list_lmoi:
                ypo = ypo - tr.val
                tpi += tr.val
                per50 = wrap(tr.per, 50) if tr.per else ['']
                stf += stt % (tr.datgr, per50[0], tr.apo, 0, tr.val, ypo)
                for per in per50[1:]:
                    stf += stb % ('', per)
            if tr.se in list_lmoi:
                ypo = ypo + tr.val
                txr += tr.val
                per50 = wrap(tr.per, 50) if tr.per else ['']
                stf += stt % (tr.datgr, per50[0], tr.se, tr.val, 0, ypo)
                for per in per50[1:]:
                    stf += stb % ('', per)
        return stf

    def kartella_tail(self, lmos, last_lines=None):
        # Ημ/νια περιγραφή χρέωση πίστωση υπόλοιπο
        Kli = namedtuple('Klin', 'no dat per lmo xr pi yp')
        if last_lines is None:
            klis = []
            per = 'Όλες οι γραμμές'
        else:
            klis = deque(maxlen=last_lines)
            per = 'τελευταίες %s γραμμές' % last_lines
        ypo = 0
        for i, tr in enumerate(sorted(self.trans, key=attrgetter('dat'))):
            j = i + 1
            if lmos == tr.apo:
                ypo = ypo - tr.val
                klis.append(Kli(j, tr.datgr, tr.per, tr.se, 0, tr.val, ypo))
            elif lmos == tr.se:
                ypo = ypo + tr.val
                klis.append(Kli(j, tr.datgr, tr.per, tr.apo, tr.val, 0, ypo))
        return lmos, per, klis

    def print_kartella(self, lmos):
        print(self.kartella(lmos))

    def print_kart(self, lmos, last_lines=None):
        if lmos not in self.lmoi:
            print(self.kartella(lmos))
            return
        lmo, lper, lins = self.kartella_tail(lmos, last_lines)
        title = '%s(%s)' % (lmo, lper)
        stb = '%10s %-60s'
        print('{:^90}'.format(title))
        for l in lins:
            val = l.xr - l.pi
            p60 = wrap(l.per, 60) if l.per else ['']
            print(f"{l.dat} {p60[0]:60}{val:8.2f} {l.yp:9.2f} {l.lmo}")
            for per in p60[1:]:
                print(stb % ('', per))

    def episkopisi(self, lmos):
        met = eso = ejo = ypo = 0
        metaf = ('ταμείο', 'ανοιγμα', 'χρεώστες', 'πιστωτές')
        for tr in self.trans:
            if lmos == tr.apo:
                if tr.se.startswith('εξοδα'):
                    ejo -= tr.val
                    ypo -= tr.val
                elif tr.se.startswith(metaf):
                    met -= tr.val
                    ypo -= tr.val
                elif tr.se.startswith('εσοδα'):
                    eso -= tr.val
                    ypo -= tr.val
                else:
                    print('problem apo', tr)
            if lmos == tr.se:
                if tr.apo.startswith('εσοδα'):
                    eso += tr.val
                    ypo += tr.val
                elif tr.apo.startswith(metaf):
                    met += tr.val
                    ypo += tr.val
                else:
                    print('problem se', tr)
        return lmos, round(met, 2), round(eso, 2), round(ejo, 2), round(ypo, 2)

    def tamiaka(self, root_lmos_tamioy='ταμείο'):
        tamd = defaultdict(lambda: {'me': 0, 'es': 0, 'ej': 0, 'yp': 0})
        metaf = ('ταμείο', 'ανοιγμα', 'χρεώστες', 'πιστωτές')
        for tr in self.trans:
            if tr.apo.startswith(root_lmos_tamioy):
                if tr.se.startswith('εξοδα'):
                    tamd[tr.apo]['ej'] -= tr.val
                    tamd[tr.apo]['yp'] -= tr.val
                elif tr.se.startswith(metaf):
                    tamd[tr.apo]['me'] -= tr.val
                    tamd[tr.apo]['yp'] -= tr.val
                elif tr.se.startswith('εσοδα'):
                    tamd[tr.apo]['es'] -= tr.val
                    tamd[tr.apo]['yp'] -= tr.val
                else:
                    print('problem apo', tr)
            if tr.se.startswith(root_lmos_tamioy):
                if tr.apo.startswith('εσοδα'):
                    tamd[tr.se]['es'] += tr.val
                    tamd[tr.se]['yp'] += tr.val
                elif tr.apo.startswith(metaf):
                    tamd[tr.se]['me'] += tr.val
                    tamd[tr.se]['yp'] += tr.val
                else:
                    print('problem se', tr)
        return tamd

    def tamiaka2list(self):
        tamd = self.tamiaka()
        lst = []
        for key, val in tamd.items():
            lst.append([key, val['me'], val['es'], val['ej']])
        return lst

    def tamiaka_print(self, root_lmos_tamioy='ταμείο'):
        tamd = self.tamiaka(root_lmos_tamioy)
        stt = '%-30s %12.2f %12.2f %12.2f %12.2f\n'
        sta = '%-30s %12s %12s %12s %12s\n'
        fin = sta % ('Λογαριασμοί', 'Μεταφορά', 'Έσοδα', 'Έξοδα', 'Υπόλοιπο')
        tme = tes = tej = typ = 0
        for key in sorted(tamd.keys()):
            me = round(tamd[key]['me'], 2)
            es = round(tamd[key]['es'], 2)
            ej = round(tamd[key]['ej'], 2)
            yp = round(tamd[key]['yp'], 2)
            if yp != 0:
                fin += stt % (key, me, es, ej, yp)
                tme += me
                tes += es
                tej += ej
                typ += yp
        fin += stt % ('Σύνολα', tme, tes, tej, typ)
        print(fin)

    def episkopisi_all(self):
        stt = '%-30s %12.2f %12.2f %12.2f %12.2f\n'
        sta = '%-30s %12s %12s %12s %12s\n'
        fin = sta % ('Λογαριασμοί', 'Μεταφορά', 'Έσοδα', 'Έξοδα', 'Υπόλοιπο')
        tots = [0, 0, 0, 0]
        for lmo in sorted(self.lmoi):
            if lmo.startswith('ταμείο'):
                vlmo = self.episkopisi(lmo)
                fin += stt % vlmo
                tots = add_lists(tots, vlmo[1:])
        tots = ['Σύνολα'] + tots
        fin += stt % tuple(tots)
        print(fin)

    def __repr__(self):
        tmp = ''
        for tran in self.trans:
            tmp += '%s\n' % tran
        return tmp


def insert_record(filename, lmoi):
    import readline

    def completer(text, state):
        options = [x for x in lmoi if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None
    dat = input('Ημερομηνία:').strip()
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    apo = input('Από       :').strip()
    se = input('Σε        :').strip()
    readline.set_completer(completer)
    val = input('Ποσό      :').strip()
    per = input('Περιγραφή :').strip()
    line = '%s|%s|%s|%s|%s\n' % (dat, apo, se, val, per)
    with open(filename, 'a') as afil:
        afil.write(line)
    print('Line %s added succesfully...')


if __name__ == '__main__':
    import os.path
    import argparse
    import sys
    pars = argparse.ArgumentParser(description=u'Minor-Accounting')
    pars.add_argument('csv', help='csv file with data')
    pars.add_argument('-a', '--Account', help='Account')
    pars.add_argument('-l', '--Lines', help='Lines', default=10)
    pars.add_argument('-d', '--Date', help='Date limit', default=None)
    pars.add_argument('-w', '--Write', help='Write to csv', default=None)
    pars.add_argument('-i', '--Insert', help='Insert', action='store_true')
    pars.add_argument('-v', '--version', action='version', version='1.1')
    pars.add_argument('-m', '--metafora', help='Metafora Ypoloipon')
    args = pars.parse_args()
    book = Book.from_file(args.csv, args.Date)
    if not os.path.isfile(args.csv):
        print('No such file : %s' % args.csv)
    if args.Insert:
        insert_record(args.csv, book.lmoi)
        sys.exit(0)
    book.print_isozygio(not_show_zero_yp=True)
    book.tamiaka_print()
    print('Τελευταίες 10 εγγραφές:')
    book.tail()
    try:
        lin = int(args.Lines)
    except Exception:
        lin = None
    if args.Account:
        if args.Account in book.lmoi:
            book.print_kart(args.Account, last_lines=lin)
            # print(book.episkopisi(args.Account))
        else:
            print(book.kartella(args.Account))
    if args.Write:
        book.write_to_file(args.Write)
    if args.metafora:
        book.metafora_ypoloipon(args.metafora, args.metafora)
    # book.metafora_ypoloipon('2018-08-31', 'tst.csv')
