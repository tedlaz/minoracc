import decimal
import textwrap
import config as cfg


def isNum(val):  # is val number or not
    """Check if val is number or not

    :param val: value to check

    :return: True if val is number else False
    """
    try:
        float(val)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """Returns a decimal. If poso is not a number or None returns dec(0)

    :param poso: the number to transofrm to decimal
    :param decimals: Number of decimals

    :return: A decimal number with specific number of decimal digits
    """
    poso = 0 if (poso is None) else poso
    tmp = decimal.Decimal(poso) if isNum(poso) else decimal.Decimal('0')
    tmp = decimal.Decimal(0) if decimal.Decimal(0) else tmp
    return tmp.quantize(decimal.Decimal(10) ** (-1 * decimals))


def triades(txt, separator='.'):
    """Help function to split digits to thousants (123456 becomes 123.456)

    :param txt: text to split
    :param separator: The separator to use

    :return: txt separated by separator in group of three

    Example::

        >>> import gr
        >>> gr.triades('abcdefg')
        'a.bcd.efg'
        >>> gr.triades('abcdefg', separator='|')
        'a|bcd|efg'
    """
    return separator.join(textwrap.wrap(txt[::-1], 3))[::-1]


def iso_dat(greek_date):
    """Μετατρέπει μια iso Ημερομηνία σε Ελληνική"""
    dd, mm, yyyy = greek_date.split('/')
    return '%s-%s-%s' % (yyyy, mm, dd)


def dec2gr(poso, decimals=2, zero_as_space=False):
    """Returns string formatted as Greek decimal (1234.56 becomes 1.234,56)

    :param poso: number to format
    :param decimals: Number of decimal digits
    :param zero_as_space: if True then zero values become one space

    :return: Greek formatted number

    Example::

        >>> import gr
        >>> gr.dec2gr('-2456')
        '-2.456,00'
        >>> gr.dec2gr(0, zero_as_space=True)
        ' '
    """
    dposo = dec(poso, decimals)
    if dposo == dec(0):
        if zero_as_space:
            return ' '
        else:
            return '0'
    sdposo = str(dposo)
    meion = '-'
    decimal_ceparator = ','
    prosimo = ''
    if sdposo.startswith(meion):
        prosimo = meion
        sdposo = sdposo.replace(meion, '')
    if '.' in sdposo:
        sint, sdec = sdposo.split('.')
    else:
        sint = sdposo
        decimal_ceparator = ''
        sdec = ''
    return prosimo + ' ' + triades(sint) + decimal_ceparator + sdec


def trs(val, threshold):
    """If absolute value of val < threshold
            return 0
       else
            return absolute value of val
    """
    val1 = abs(val)
    # print("val: %s, threshold: %s, val1: %s" % (val, threshold, val1))
    return dec(0) if val1 <= dec(threshold) else dec(val1)


def vat_best_mach(vals, vats, thres):
    """Find best mach between list of values and a list of vat values

    :param vals: list of values
    :param vats: list of vat values
    """
    assert len(vats) <= len(vals)  # vat lines can't be more than val lines
    gvata = []
    setvat = set()
    setval = set()
    for i, vt in enumerate(vats):  # loop over list of vat values
        gvt = []
        for j, vl in enumerate(vals):  # loop over list of values
            gvals = []
            for sv in cfg.VATPOSN:  # loop over normal vat rates
                fvv = trs(vl * sv / dec(100) - vt, thres)
                gvals.append(fvv)
            gvt.append(gvals)
            if 0 in gvals:
                # idx = gvals.index(0)
                # print('Found:', i, vt, j, vl, VATPOSN[idx])
                setvat.add(i)
                setval.add(j)
        gvata.append(gvt)
    # print(gvata, setvat, setval)
    assert len(setvat) == len(setval)
    return len(setvat) == len(vats)

def is_afm(a):
    '''
    Algorithmic validation of Greek Vat Numbers
    '''
    if not isNum(a):
        return False
    if len(a) != 9:
        return False
    b = int(a[0]) * 256 + int(a[1]) * 128 + int(a[2]) * 64 + int(a[3]) * 32 + \
        int(a[4]) * 16 + int(a[5]) * 8 + int(a[6]) * 4 + int(a[7]) * 2
    c = b % 11
    d = c % 10
    return d == int(a[8])
