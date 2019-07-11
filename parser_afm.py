def parse_afm(fil, enc='WINDOWS-1253'):
    # Create list with lines to exclude
    EXC = (' ' * 109 + 'Σελίδα',
           ' ' * 44 + 'Κατηγορία ',
           '  Oνομα / Επωνυμία ',
           '  ----------------------------------------- ',
    )
    SEPON = slice(2, 44)
    SCODE = slice(54, 66)
    SAFM = slice(87, 96)
    epo = cod = afm = ''
    res = {}
    with open(fil, encoding=enc) as ofil:
        for lin in ofil:
            llin = len(lin)
            if llin < 86:
                continue
            elif lin.startswith(EXC):  # Exclude lines
                continue
            epo = lin[SEPON].strip()
            cod = lin[SCODE].strip()
            afm = lin[SAFM].strip()
            if cod[2] == '.':
                # res.append((epo, cod, afm))
                res[cod] = afm
    return res


if __name__ == '__main__':
    fil = "/home/ted/Downloads/afm.txt"
    prs = parse_afm(fil)
    for lin in prs.keys():
        print(lin, prs[lin])
    print(len(prs))
