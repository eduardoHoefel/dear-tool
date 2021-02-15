import scipy.stats as sc
import log

from estimators.known_formula import KnownFormula

class SynteticDatafile():

    def __init__(self, m, s, samples):
        self.samples = samples
        self.m = m
        self.s = s
        self.f = sc.norm.pdf
        self.generate()
        self.density = KnownFormula(self).estimate()

    def generate(self):
        self.data = sc.norm.rvs(self.m, self.s, self.samples)

    def get_data(self):
        return self.data

    def __str__(self):
        return "[{}, {}, {}]".format(self.samples, self.m, self.s)

