import numpy as np
import scipy as sc

class Crude():

    def __init__(self, data):
        self.x = data['x']
        self.name = 'crude'

    def estimate(self):
        true_mean = np.mean(self.x)
        true_std_deviation = np.std(self.x)

        p_x = sc.stats.norm.pdf(self.x, true_mean, true_std_deviation)
        return -np.mean(np.where(p_x != 0, np.log2(p_x), 0))
