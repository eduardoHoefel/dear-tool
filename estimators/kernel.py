import numpy as np
from sklearn.neighbors import KernelDensity
from estimators.estimator import Estimator

class Kernel(Estimator):

    def get_name():
        return "Kernel"

    def get_parameters():
        return ['kernel', 'bandwidth']

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.x = datafile.data
        self.kernel = parameters['kernel'] if 'kernel' in parameters else 'gaussian'
        self.bandwidth = parameters['bandwidth'] if 'bandwidth' in parameters else 0.4
        self.id = "KDE({}, {})".format(self.kernel, self.bandwidth)
        self.name = self.id

    def estimate(self):

        kde = KernelDensity(bandwidth=self.bandwidth, kernel=self.kernel).fit(self.x[:, np.newaxis])
        r = kde.score_samples(self.x[:, np.newaxis])
        p_x = np.exp(r)

        return Estimator.get_shannon_entropy(p_x)
