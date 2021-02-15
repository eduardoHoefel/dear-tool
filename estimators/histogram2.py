import numpy as np
from estimators.estimator import Estimator

class Histogram2(Estimator):

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.bins = 'auto'
        self.name = 'hist2'

    def estimate(self):
        max_v = max(self.x)
        min_v = min(self.x)
        bins = 9
        bin_size = (max_v - min_v) / bins
        ys_freq = np.zeros(bins)
        ys_hist = []
        for i in range(bins+1):
            h_v = min_v + (i * bin_size)
            ys_hist.append(h_v)

        for i in self.x:
            v_bin = -1
            if i == max_v:
                ys_freq[-1] += 1
                continue

            for j in ys_hist:
                if i < j:
                    ys_freq[v_bin] += 1
                    break
                v_bin += 1

        p_y = ys_freq / len(self.x)

        acc = 0
        if bin_size > 0:
            for p in p_y:
                if p/bin_size > 0:
                    print("p: {}, acc: {}, p / bin_size: {}, add: {}".format(p, acc, p / bin_size, p * np.log2(p / bin_size)))
                    acc += p * np.log2(p / bin_size)

        return -acc
