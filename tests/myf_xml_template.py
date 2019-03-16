xmn = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<packages>\n'
       '{package}\n'
       '</packages>')
xpk = ('  <package actor_afm="{afm}" month="{month}" year="{year}" branch="{branch}">\n'
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
       '        <cashreg_id>{casreg_id}</cashreg_id>\n'
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


def main(data, actor_afm, year, branch='', action='replace'):
    dats = {1: '%s-03-31' % year, 2: '%s-06-30' % year,
            3: '%s-09-30' % year, 4: '%s-12-31' % year}
    print(dats)
    {1: {}, 2:{}}
    for per, pdat in data.items():



if __name__ == "__main__":
    aa = {'afm': '123123123', 'amount': 100, 'tax': 24, 'invoices': 2, 'note': 'normal', 'date': '2018-03-31'}
    ss = [aa, aa, aa]
    st1  = ''
    for a in ss:
        st1 += xpe.format(**a)
    print(st1)
    main('fd', '123123123', 2018)