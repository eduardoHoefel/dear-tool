import numpy as np
import scipy as sc

def create_g_log(f, x, m, s):
    g = lambda x:f(x, m, s)

    def g_log(x):
        temp = g(x)

        if temp == 0:
            return 0

        return temp * np.log2(temp)

    return g_log

class KnownFormula():

    def __init__(self, data):
        f = data['f']
        x = data['x']
        m = data['m']
        s = data['s']

        self.g_log = create_g_log(f, x, m, s)
        self.name = "known"

    def estimate(self):

        i,err = sc.integrate.quad(self.g_log, -np.inf, np.inf)

        return -i
