from enums import MyfCat
from utils import d2c
from logger import logger


xmn = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<packages>\n'
       '{package}\n'
       '</packages>')

xpk = ('  <package actor_afm="{aafm}" month="{month}" year="{year}" branch="{branch}">\n'
       '{data}'
       '  </package>')

oex = ('    <otherExpenses>\n'
       '      <amount>{amount}</amount>\n'
       '      <tax>{tax}</tax>\n'
       '      <date>{date}</date>\n'
       '    </otherExpenses>\n')

csr = ('    <groupedCashRegisters action="{action}">\n'
       '{data}'
       '    </groupedCashRegisters>\n')

csh = ('      <cashregister>\n'
       '        <cashreg_id>{cashreg_id}</cashreg_id>\n'
       '        <amount>{amount}</amount>\n'
       '        <tax>{tax}</tax>\n'
       '        <date>{date}</date>\n'
       '      </cashregister>\n')

grv = ('    <groupedRevenues action="{action}">\n'
       '{data}'
       '    </groupedRevenues>\n')

rve = ('      <revenue>\n'
       '        <afm>{afm}</afm>\n'
       '        <amount>{amount}</amount>\n'
       '        <tax>{tax}</tax>\n'
       '        <invoices>{invoices}</invoices>\n'
       '        <note>{note}</note>\n'
       '        <date>{date}</date>\n'
       '      </revenue>\n')

gxp = ('    <groupedExpenses action="{action}">\n'
       '{data}'
       '    </groupedExpenses>\n')

xpe = ('      <expense>\n'
       '        <afm>{afm}</afm>\n'
       '        <amount>{amount}</amount>\n'
       '        <tax>{tax}</tax>\n'
       '        <invoices>{invoices}</invoices>\n'
       '        <note>{note}</note>\n'
       '        <nonObl>0</nonObl>\n'
       '        <date>{date}</date>\n'
       '      </expense>\n')


def create_xml(data, actor_afm, year, fpath, branch='', taction='replace'):
    dats = {1: '%s-03-31' % year, 2: '%s-06-30' % year,
            3: '%s-09-30' % year, 4: '%s-12-31' % year}
    month = {1: 3, 2: 6, 3: 9, 4: 12}
    total_package = ''
    for period in sorted(data.keys()):
        typs = data[period]
        package = {'aafm': actor_afm, 'year': year,
                   'month': month[period], 'branch': branch}
        ityps = [i.value for i in typs.keys()]
        package['data'] = ''
        vlt = {}
        for ityp in sorted(ityps):
            typ = MyfCat(ityp)
            afms = typs[typ]
            for afm in sorted(afms.keys()):
                decrs = afms[afm]
                for decr, vals in decrs.items():
                    dval = {'afm': afm, 'amount': d2c(vals[0]),
                            'tax': d2c(vals[1]), 'invoices': vals[2],
                            'note': decr, 'date': dats[period],
                            'cashreg_id': ''}
                    if typ == MyfCat.PEL:
                        vlt[ityp] = vlt.get(ityp, '') + rve.format(**dval)
                    elif typ == MyfCat.PELLIA:
                        vlt[ityp] = vlt.get(ityp, '') + csh.format(**dval)
                    elif typ == MyfCat.PRO:
                        vlt[ityp] = vlt.get(ityp, '') + xpe.format(**dval)
                    elif typ == MyfCat.PROCUB:
                        vlt[ityp] = vlt.get(ityp, '') + oex.format(**dval)
                    else:
                        logger.critical('Critical Error!!!')
        fst = ''
        for key, val in vlt.items():
            if key == MyfCat.PEL.value:
                fst += grv.format(data=val, action=taction)
            elif key == MyfCat.PELLIA.value:
                fst += csr.format(data=val, action=taction)
            elif key == MyfCat.PRO.value:
                fst += gxp.format(data=val, action=taction)
            elif key == MyfCat.PROCUB.value:
                fst += val
        package['data'] += fst
        xpkg = xpk.format(**package)
        total_package += xpkg
    xml_file = fpath + ('%s-%s.xml' % (year, actor_afm))
    with open(xml_file, 'w', encoding='utf-8') as fil:
        fil.write(xmn.format(package=total_package))


if __name__ == "__main__":
    import parse2book as p2b
    el_file = "/home/ted/tmp/fpa/el201812.txt"
    ee_file = "/home/ted/tmp/fpa/ee201812.txt"
    afm_file = "/home/ted/tmp/totals/afm.txt"
    fpath = '/home/ted/tmp/'
    bk1 = p2b.parse2book(el_file, ee_file, afm_file)
    myf_data = bk1.myf_totals(2018)
    create_xml(myf_data, "091767623", 2018, fpath)
