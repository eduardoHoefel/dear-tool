import numpy as np
from estimators.estimator import Estimator

class AdaptiveHistogram(Estimator):

    def get_name():
        return "Adaptive Histogram"

    def get_parameters():
        return ['population_method', 'bin_population']

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)
        default = 'auto'

        self.x = datafile.data
        self.choose_method(parameters)
        self.name = "AH({} [{}])".format(str(self.bin_population).rjust(5), "AUTO" if self.bin_population == self.get_auto_bin_population() else "MANUAL")

    def choose_method(self, parameters):
        self.method = parameters['population_method'] if 'population_method' in parameters else 'default'
        self.calculate_population(parameters)

    def get_auto_bin_population(self):
        import math
        samples = len(self.x)
        P = 0.29807168451945776
        Q = 0.408666269458574  
        R = -18.655570741600304
        C = 9.1206903384208    
        f = lambda x: math.log(x) * math.pow(x, P) * Q * (1+R/x) + C
        return round(f(samples))
        
    def calculate_population(self, parameters):
        if self.method == 'default':
            self.method = 'manual' if 'bin_population' in parameters and parameters['bin_population'] is not None else 'auto'

        if self.method == 'auto':
            self.bin_population = self.get_auto_bin_population()
        else:
            self.bin_population = parameters['bin_population']

        self.calculate_bins()

    def calculate_bins(self):
        self.bins = int(len(self.x) / self.bin_population)

    def estimate(self):
        self.x.sort()

        ys_freq = np.zeros(self.bins)
        ys_hist = np.zeros(self.bins)

        bins = []

        cur_bin = []
        for i in range(len(self.x)):
            j = self.x[i]
            cur_bin.append(j)
            if i + 1 == len(self.x) or (len(bins) + 1 < self.bins and (i - 1 == int((len(bins) + 1) * self.bin_population))):
                bins.append(cur_bin)
                cur_bin = []

        last_border = min(bins[0])
        for i in range(len(bins)-1):
            b_left = bins[i]
            b_right = bins[i+1]
            left_border = last_border
            right_border = np.mean([max(b_left), min(b_right)])
            ys_hist[i] = right_border - left_border
            ys_freq[i] = len(bins[i])

            last_border = right_border

        left_border = last_border
        right_border = max(bins[-1])
        ys_hist[-1] = right_border - left_border
        ys_freq[-1] = len(bins[-1])

        p_y = ys_freq / len(self.x)

        acc = 0
        it = np.nditer(p_y, flags=['f_index'])
        for p in it:
            if ys_hist[it.index] != 0 and p / ys_hist[it.index] != 0:
                acc += p * np.log2(p / ys_hist[it.index])

        return -acc
