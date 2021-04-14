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
        self.id = "HIST({})".format(str(self.bins).rjust(5))
        self.name = "HIST({} [{}])".format(str(self.bins).rjust(5), 'AUTO' if self.is_auto(self.bins) else 'MANUAL')

    def get_bin_size(self, bins):
        ys_freq, ys_hist = np.histogram(self.x, bins=bins)
        bin_size = ys_hist[1] - ys_hist[0]
        return bin_size

    def is_auto(self, bins):
        b1 = self.get_bin_size('auto')
        b2 = self.get_bin_size(bins)
        return b1 == b2

    def get_shannon_entropy(c, bin_sizes=1):
        c = c / np.sum(c)
        c = c[np.nonzero(c)]

        H = -sum(c * np.log2(c / bin_sizes))

        return H

    def estimate(self):
        self.ys_freq, self.ys_hist = np.histogram(self.x, bins=self.bins)
        self.bin_size = self.ys_hist[1] - self.ys_hist[0]
        if self.bin_size == 0:
            return 0

        return Histogram.get_shannon_entropy(self.ys_freq, self.bin_size)
