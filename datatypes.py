
def natural(value):
    if float(value) == 0:
        return 1

    return positive(value)

def positive(value):
    return abs(myfloat(value))

def myfloat(value):
    if float(value) == int(float(value)):
        return int(value)

    return float(value)


'''positive float'''
def pfloat(value):
    return positive(value)

'''natural float'''
def nfloat(value):
    return natural(myfloat(value))

'''positive int '''
def pint(value):
    return positive(int(value))

'''natural int'''
def nint(value):
    return natural(int(value))
