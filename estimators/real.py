import numpy as np
import scipy as sc

class Real():

    def __init__(self, data):
        self.x = data['x']
        self.m = data['m']
        self.s = data['s']
        self.name = 'true'

    def estimate(self):
        p_x = sc.stats.norm.pdf(self.x, self.m, self.s)

        return -np.mean(np.where(p_x != 0, np.log2(p_x), 0))
