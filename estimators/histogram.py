import numpy as np
from estimators.estimator import Estimator

class Histogram(Estimator):

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.bins = 'auto'
        self.name = 'hist'

    def estimate(self):
        ys_freq, ys_hist = np.histogram(self.x, bins=9)
        bin_size = ys_hist[1] - ys_hist[0]

        p_y = ys_freq / len(self.x)

        acc = 0
        if bin_size > 0:
            for p in p_y:
                if p/bin_size > 0:
                    acc += p * np.log2(p / bin_size)

        return -acc
