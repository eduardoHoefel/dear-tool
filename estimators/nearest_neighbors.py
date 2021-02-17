import numpy as np
from sklearn.neighbors import NearestNeighbors
from estimators.estimator import Estimator

class NN(Estimator):

    def get_name():
        return "Neares Neighbors"

    def get_parameters():
        return []

    def __init__(self, datafile, parameters={}):
        super().__init__(datafile, parameters)

        self.data = datafile.data
        self.name = "nn"

    def estimate(self):
        return 0
