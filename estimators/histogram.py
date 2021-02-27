import numpy as np
from estimators.estimator import Estimator

class Histogram(Estimator):

    def get_name():
        return "Histogram"

    def get_parameters():
        return ['bins_method', 'bins']

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.bins_method = parameters['bins_method'] if 'bins_method' in parameters else 'default'
        self.bins = 'auto' if self.bins_method == 'default' else parameters['bins'] if self.bins_method == 'manual' else self.bins_method
        self.name = "HIST({} [{}])".format(str(self.bins).rjust(5), 'AUTO' if self.is_auto(self.bins) else 'MANUAL')

    def get_bin_size(self, bins):
        ys_freq, ys_hist = np.histogram(self.x, bins=bins)
        bin_size = ys_hist[1] - ys_hist[0]
        return bin_size

    def is_auto(self, bins):
        b1 = self.get_bin_size('auto')
        b2 = self.get_bin_size(bins)
        return b1 == b2

    def estimate(self):
        ys_freq, ys_hist = np.histogram(self.x, bins=self.bins)
        bin_size = ys_hist[1] - ys_hist[0]

        p_y = ys_freq / len(self.x)

        acc = 0
        if bin_size > 0:
            for p in p_y:
                if p/bin_size > 0:
                    acc += p * np.log2(p / bin_size)

        return -acc
