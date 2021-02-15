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
        self.kernel = parameters['kernel']
        self.bandwidth = parameters['bandwidth']
        self.name = "KDE({}, {})".format(self.kernel, self.bandwidth)

    def estimate(self):

        kde = KernelDensity(bandwidth=self.bandwidth, kernel=self.kernel).fit(self.x[:, np.newaxis])
        p_x = np.exp(kde.score_samples(self.x[:, np.newaxis]))

        return -np.mean(np.where(p_x > 0, np.log2(p_x), 0))
