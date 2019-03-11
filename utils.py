import config as cfg


def trs(val, threshold):
    """If absolute value of val < threshold
            return 0
       else
            return absolute value of val
    """
    val1 = round(abs(val), 2)
    # print("val: %s, threshold: %s, val1: %s", (val, threshold, val1))
    return 0 if val1 <= threshold else val1


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
                fvv = trs(vl * sv / 100.0 - vt, thres)
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
