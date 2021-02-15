import numpy as np
import scipy as sc
from estimators.estimator import Estimator

class Crude(Estimator):

    def get_name():
        return "Crude"

    def get_parameters():
        return []

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.name = 'crude'

    def estimate(self):
        true_mean = np.mean(self.x)
        true_std_deviation = np.std(self.x)

        p_x = sc.stats.norm.pdf(self.x, true_mean, true_std_deviation)
        return -np.mean(np.where(p_x != 0, np.log2(p_x), 0))
