import numpy as np
import math
from sklearn.neighbors import NearestNeighbors
from estimators.estimator import Estimator

class NN(Estimator):

    def get_name():
        return "Nearest Neighbors"

    def get_parameters():
        return ['neighbors_method', 'neighbors']

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.data = datafile.data
        self.choose_method(parameters)
        self.id = "NN({})".format(str(self.neighbors).rjust(5))
        self.name = "NN({} [{}])".format(str(self.neighbors).rjust(5), "AUTO" if self.neighbors == self.get_auto_neighbors() else "MANUAL")

    def choose_method(self, parameters):
        self.method = parameters['neighbors_method'] if 'neighbors_method' in parameters else 'default'
        self.calculate_neighbors(parameters)
        
    def calculate_neighbors(self, parameters):
        if self.method == 'default':
            self.method = 'manual' if 'neighbors' in parameters and parameters['neighbors'] is not None else 'auto'

        if self.method == 'auto':
            self.neighbors = self.get_auto_neighbors()
        else:
            self.neighbors = parameters['neighbors']

    def get_auto_neighbors(self):
        #maior n, menor e
        #maior divisao, menor n
        #maior divisao, maior e
        x = np.std(self.data)
        y = len(self.data)

        power_x = -2
        power_y = 1
        fraction_m = 0.11899

        return round(math.pow(x, power_x) * math.pow(y, power_y) * fraction_m)

    def estimate(self):
        self.data.sort()

        if self.neighbors == 0:
            return 0

        nbrs = NearestNeighbors(n_neighbors=self.neighbors+1, algorithm='ball_tree').fit(self.data[:, np.newaxis])
        distances, indices = nbrs.kneighbors(self.data[:, np.newaxis])

        p_x = np.array([x[-1] for x in distances])
        return Estimator.get_shannon_entropy(p_x)
