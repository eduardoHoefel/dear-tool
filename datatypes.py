
def natural(value):
    if float(value) == 0:
        return 1

    return positive(value)

def positive(value):
    return abs(myfloat(value))

def myint(value):
    return int(float(value))

def myfloat(value):
    if float(value) == myint(value):
        return myint(value)

    return float(value)


'''positive float'''
def pfloat(value):
    return positive(value)

'''natural float'''
def nfloat(value):
    return natural(myfloat(value))

'''positive int '''
def pint(value):
    return positive(myint(value))

'''natural int'''
def nint(value):
    return natural(myint(value))
