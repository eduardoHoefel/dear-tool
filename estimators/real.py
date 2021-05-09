import numpy as np
import scipy as sc
from estimators.estimator import Estimator

class Real(Estimator):

    def get_name():
        return "Real"

    def get_parameters():
        return []

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.m = datafile.m
        self.s = datafile.s
        self.f = datafile.f
        self.id = 'true'
        self.name = self.id

    def estimate(self):
        p_x = self.f(self.x, self.m, self.s)
        return Estimator.get_shannon_entropy(p_x)
