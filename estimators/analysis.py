import numpy as np

class EstimationAnalysis():

    def __init__(self, estimation, real_value):
        self.estimation = 0 if estimation is None else estimation
        self.real_value = real_value
        self.review()

    def review(self):
        errors = {}

        self.raw = abs(self.real_value - self.estimation)
        self.relative = self.raw/self.real_value
        if self.relative == 0:
            self.score = 100
        else:
            try:
                self.score =  max(0, -int(np.log2(self.relative)))
            except:
                self.score =  0

        if self.score is None:
            self.score = 0

