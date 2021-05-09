import scipy.stats as sc
import numpy as np
import log

from datafiles.datafile import Datafile
from estimators.known_formula import KnownFormula

class SyntheticDatafile(Datafile):

    def generate_data(dist, dist_params, loc, scale, samples, seed=None):
        if seed is not None:
            np.random.seed(seed) 

        data = dist.rvs(dist_params, loc, scale, samples)
        return data

    def __init__(self, dist, dist_params, loc, scale, samples, seed=None):
        pdf = dist.pdf
        d = SyntheticDatafile.generate_data(dist, dist_params, loc, scale, samples, seed)
        self.dist = dist
        self.name = "{}{}, {} samples, loc={}, scale={}".format(str(dist), "({})".format(", ".join([str(x) for x in dist_params])) if len(dist_params) > 0 else "", samples, loc, scale)

        pdf_params = dist_params[:]
        pdf_params.append(loc)
        pdf_params.append(scale)

        super().__init__(d, pdf, pdf_params)
        self.set_density(KnownFormula(self).estimate())

    def __str__(self):
        return self.name

