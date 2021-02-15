import numpy as np
from estimators.estimator import Estimator

class AdaptiveHistogram(Estimator):

    def get_parameters():
        return ['bins', 'bin_population']

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.bins = parameters['bins']
        self.bin_population = parameters['bin_population']

        self.name = "AH({}, {})".format(int(self.bins), int(self.bin_population))

    def estimate(self):
        self.x.sort()

        ys_freq = np.zeros(self.bins)
        ys_hist = np.zeros(self.bins)

        cur_bin_i = 0
        cur_bin = []
        for i in range(len(self.x)):
            j = self.x[i]
            cur_bin.append(j)
            if (cur_bin_i + 1 == self.bins and i + 1 == len(self.x)) or (cur_bin_i + 1 < self.bins and (i - 1 == int((cur_bin_i + 1) * self.bin_population))):
                ys_hist[cur_bin_i] = max(cur_bin) - min(cur_bin)
                ys_freq[cur_bin_i] = len(cur_bin)
                cur_bin_i += 1
                cur_bin = []

        p_y = ys_freq / len(self.x)

        acc = 0
        it = np.nditer(p_y, flags=['f_index'])
        for p in it:
            if ys_hist[it.index] != 0 and p / ys_hist[it.index] != 0:
                acc += p * np.log2(p / ys_hist[it.index])

        return -acc
