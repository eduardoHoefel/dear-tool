import scipy.stats as sc
import log

from datafiles.datafile import Datafile
from estimators.known_formula import KnownFormula

class SyntheticDatafile(Datafile):

    def generate_data(m, s, samples):
        data = sc.norm.rvs(m, s, samples)
        return data

    def __init__(self, m, s, samples):
        f = sc.norm.pdf
        d = SyntheticDatafile.generate_data(m, s, samples)
        super().__init__(d, m, s, f)
        self.set_density(KnownFormula(self).estimate())

    def __str__(self):
        return "[{}, {}, {}]".format(self.samples, self.m, self.s)

