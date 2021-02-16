
class Estimator():

    def __init__(self, datafile, parameters):
        self.datafile = datafile
        self.parameters = parameters
        self.output = None

    def run(self):
        self.output = self.estimate()

    def estimate(self):
        return 0
