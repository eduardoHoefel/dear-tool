from estimators.analysis import EstimationAnalysis
import numpy as np

class Estimator():

    def __init__(self, datafile, parameters):
        self.datafile = datafile
        self.parameters = parameters
        self.output = None

    def run(self):
        self.output = self.estimate()

    def analyse(self, real_value):
        self.review = EstimationAnalysis(self.output, real_value)

    def get_shannon_entropy(c, bin_sizes=1):
        c = c[np.nonzero(c)]
        H = -np.mean(np.log2(c))

        return H

    def get_mutual_information(p_k, p_l, p_k_l):
        h_k = self.get_shannon_entropy(p_k)
        h_l = self.get_shannon_entropy(p_l)
        h_kl = self.get_shannon_entropy(p_kl)

        H = h_k + h_l - h_kl

        return H











    def get_sort_value(self, key):
        if key == 'name':
            return self.name

        if key == 'bin_population':
            return self.bin_population

        if key == 'result':
            return self.output

        if key == 'score':
            return self.review.raw

        return self.name

    def estimate(self):
        return 0

    def get_parameter_range(E, parameter, datafile, window):
        expected = datafile.density

        left = None
        last_density = None
        direction = None
        #print(expected)
        while True:
            right = 0 if left is None else int(left+window/2)
            p = {parameter: right}
            e = E(datafile, p)
            r = e.estimate()
            #print("{}: {}".format(p, r))
            if last_density is not None:
                if r == expected or ((expected - last_density) / (expected - r)) < 0:
                    return {'from': left, 'to': left + window, 'step': 1}
                if direction is not None and direction / (r - last_density) < 0:
                    return {'from': int(left - window/2), 'to': int(left+window/2), 'step': 1}

                direction = r - last_density
            last_density = r
            left = right

