import numpy as np
from sklearn.neighbors import KernelDensity
from estimators.estimator import Estimator

class Kernel(Estimator):

    def get_name():
        return "Kernel"

    def get_parameters():
        return ['kernel', 'bandwidth']

    def get_default_experiment_parameters(datafile):
        auto = Kernel(datafile)
        return {'bandwidth': {'from': 0.1, 'to': 5, 'step': 0.1}, 'auto': auto}

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.kernel = parameters['kernel'] if 'kernel' in parameters else 'gaussian'
        self.bandwidth = parameters['bandwidth'] if 'bandwidth' in parameters else 1.0
        bandwidth_str = "{:.2f}".format(self.bandwidth)
        self.auto = self.is_auto(self.bandwidth, parameters)
        self.id = "KDE({} [{}])".format(bandwidth_str, 'AUTO' if self.auto else 'MANUAL')
        self.name = self.id
        self.plot_name_short = bandwidth_str
        self.plot_name_full = self.id

    def is_auto(self, bandwidth, parameters):
        if 'auto' in parameters.keys():
            return bandwidth == parameters['auto'].bandwidth

        return bandwidth == 1.0

    def pde(self, x):
        if type(x) is np.ndarray or type(x) is list:
            return [self.pde(xi) for xi in x]

        i = np.where(self.x == x)
        if len(i) == 0:
            return 0

        i = i[0]
        if len(i) == 0:
            return 0
        i = i[0]

        return self.density[i]


    def estimate(self):

        kde = KernelDensity(bandwidth=self.bandwidth, kernel=self.kernel).fit(self.x[:, np.newaxis])
        r = kde.score_samples(self.x[:, np.newaxis])
        p_x = np.exp(r)
        self.density = p_x

        return Estimator.get_shannon_entropy(p_x)
