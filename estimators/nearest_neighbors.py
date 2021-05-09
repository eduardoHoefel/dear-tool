import numpy as np
import math
from sklearn.neighbors import NearestNeighbors
from estimators.estimator import Estimator
from estimators.histogram import Histogram

class NN(Estimator):

    def get_name():
        return "Nearest Neighbors"

    def get_parameters():
        return ['neighbors_method', 'neighbors']

    def get_default_experiment_parameters(datafile):
        auto = NN(datafile, {})
        return {'neighbors': {'from': 1, 'to': datafile.samples, 'step': 1}, 'auto': auto}

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.data = datafile.data
        self.choose_method(parameters)
        self.id = "NN({})".format(str(self.neighbors).rjust(5))
        self.auto = self.neighbors == (parameters['auto'].neighbors if 'auto' in parameters.keys() else self.get_auto_neighbors())
        self.name = "NN({} [{}])".format(str(self.neighbors).rjust(5), "AUTO" if self.auto else "MANUAL")
        self.plot_name_short = str(self.neighbors)
        self.plot_name_full = self.id

    def choose_method(self, parameters):
        self.method = parameters['neighbors_method'] if 'neighbors_method' in parameters.keys() else 'default'
        self.calculate_neighbors(parameters)
        
    def calculate_neighbors(self, parameters):
        if self.method == 'default':
            self.method = 'manual' if 'neighbors' in parameters.keys() and parameters['neighbors'] is not None else 'auto'

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

        return max(1, min(y-1, round(math.pow(x, power_x) * math.pow(y, power_y) * fraction_m)))

    def pde(self, x):
        if type(x) is np.ndarray or type(x) is list:
            return [self.pde(xi) for xi in x]

        index = np.where(self.data == x)
        if len(index) == 0:
            return 0
        index = index[0]
        if len(index) == 0:
            return 0
        index = index[0]

        r = self.neighbors/ (2 * len(self.data) * self.distances[index])
        return r

    def estimate(self):
        self.data.sort()

        if self.neighbors == 0:
            return 0

        nbrs = NearestNeighbors(n_neighbors=self.neighbors+1, algorithm='ball_tree').fit(self.data[:, np.newaxis])
        distances, indices = nbrs.kneighbors(self.data[:, np.newaxis])
        self.distances = [x[-1] for x in distances]

        p_x = np.array(self.distances)
        self.density = p_x
        #p_x = p_x * r
        return Estimator.get_shannon_entropy(p_x)
