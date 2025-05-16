def SH1_CURVE(t, x4):
    """Function calculates time delay for HU1"""
    if t <= 0.0:
        return 0.0
    elif t < x4:
        return (t/x4)**2.5
    else:
        return 1.0

def SH2_CURVE(t, x4):
    """Function calculates time delay for HU2"""
    if t <= 0.0:
        return 0.0
    elif t <= x4:
        return 0.5*(t/x4)**2.5
    elif t < 2*x4:
        return 1-0.5*(2-t/x4)**2.5
    else:
        return 1.0