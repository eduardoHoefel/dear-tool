import numpy as np
from estimators.estimator import Estimator

class Histogram(Estimator):

    def get_name():
        return "Histogram"

    def get_parameters():
        return ['bins_method', 'bins']

    def get_default_experiment_parameters(datafile):
        auto = Histogram(datafile, {})
        return {'bins_method': "manual", 'bins': {'from': 5, 'to': datafile.samples*5, 'step': 1}, 'auto': auto}

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.bins_method = parameters['bins_method'] if 'bins_method' in parameters.keys() else 'default'
        self.bins = 'auto' if self.bins_method == 'default' else parameters['bins'] if self.bins_method == 'manual' else self.bins_method
        if self.bins == 'auto':
            self.bins = self.get_auto_bins()

        self.id = "HIST({})".format(str(self.bins).rjust(5))
        self.auto = self.is_auto(self.bins, parameters)
        self.name = "HIST({} [{}])".format(str(self.bins).rjust(5), 'AUTO' if self.auto else 'MANUAL')
        self.plot_name_short = str(self.bins)
        self.plot_name_full = self.id

    def get_auto_bins(self):
        ys_freq, ys_hist = np.histogram(self.x, bins='auto')
        return len(ys_freq)

    def is_auto(self, bins, parameters):
        if 'auto' in parameters.keys():
            return bins == parameters['auto'].bins

        return bins == self.get_auto_bins()

    def get_shannon_entropy(c, bin_sizes=1):
        c = c / np.sum(c)
        if type(bin_sizes) is np.ndarray:
            bin_sizes = bin_sizes[np.nonzero(c)]

        c = c[np.nonzero(c)]

        H = -sum(c * np.log2(c / bin_sizes))

        return H

    def pde(self, x):
        if type(x) is np.ndarray or type(x) is list:
            return [self.pde(xi) for xi in x]

        for i, h in enumerate(self.ys_hist[:-1]):
            h2 = self.ys_hist[i+1]
            if x >= h and x <= h2:
                return self.ys_freq[i]/(self.bin_widths[i]*len(self.x))

        return 0

    def get_bars(self):
        points = []
        heights = []

        for i, h in enumerate(self.ys_hist[:-1]):
            h2 = self.ys_hist[i+1]
            avg = (h2+h)/2
            points.append(avg)
            heights.append(self.pde(avg))

        return points, heights, self.bin_widths

    def estimate(self):
        if self.bins <= 0:
            return 0

        self.ys_freq, self.ys_hist = np.histogram(self.x, bins=self.bins)
        self.bin_size = self.ys_hist[1] - self.ys_hist[0]
        self.bin_widths = [self.bin_size for y in self.ys_freq]

        if self.bin_size == 0:
            return 0

        return Histogram.get_shannon_entropy(self.ys_freq, self.bin_size)
