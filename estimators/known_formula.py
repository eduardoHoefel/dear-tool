import numpy as np
import scipy as sc
from estimators.estimator import Estimator

def create_g_log(f, x, m, s):
    g = lambda x:f(x, m, s)

    def g_log(x):
        temp = g(x)

        if temp == 0:
            return 0

        return temp * np.log2(temp)

    return g_log

class KnownFormula(Estimator):

    def get_name():
        return "Known Formula"

    def get_parameters():
        return []

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        x = datafile.data
        f = datafile.f
        m = datafile.m
        s = datafile.s

        self.g_log = create_g_log(f, x, m, s)
        self.name = "known"

    def estimate(self):

        i,err = sc.integrate.quad(self.g_log, -np.inf, np.inf)

        return -i
