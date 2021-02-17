from estimators.analysis import EstimationAnalysis

class Estimator():

    def __init__(self, datafile, parameters):
        self.datafile = datafile
        self.parameters = parameters
        self.output = None

    def run(self):
        self.output = self.estimate()

    def analyse(self, real_value):
        self.review = EstimationAnalysis(self.output, real_value)

    def get_sort_value(self, key):
        if key == 'name':
            return self.name

        if key == 'bin_population':
            return self.bin_population

        if key == 'result':
            return self.output

        if key == 'score':
            return self.review.raw

        return self.name

    def estimate(self):
        return 0
