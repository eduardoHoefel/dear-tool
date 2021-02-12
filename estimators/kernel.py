import numpy as np
from sklearn.neighbors import KernelDensity

class Kernel:

    def __init__(self, data):
        self.x = data['x']
        self.kernel = 'gaussian'
        self.bandwidth = 0.4
        self.name = "KDE({}, {})".format(self.kernel, self.bandwidth)

    def estimate(self):

        kde = KernelDensity(bandwidth=self.bandwidth, kernel=self.kernel).fit(self.x[:, np.newaxis])
        p_x = np.exp(kde.score_samples(self.x[:, np.newaxis]))

        return -np.mean(np.where(p_x > 0, np.log2(p_x), 0))
