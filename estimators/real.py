import numpy as np
import scipy as sc
from estimators.estimator import Estimator

class Real(Estimator):

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.m = datafile.m
        self.s = datafile.s
        self.name = 'true'

    def estimate(self):
        p_x = sc.stats.norm.pdf(self.x, self.m, self.s)

        return -np.mean(np.where(p_x != 0, np.log2(p_x), 0))
