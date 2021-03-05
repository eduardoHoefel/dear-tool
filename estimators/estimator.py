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

    def get_parameter_range(E, parameter, datafile, window):
        expected = datafile.density

        left = None
        last_density = None
        direction = None
        #print(expected)
        while True:
            right = 0 if left is None else int(left+window/2)
            p = {parameter: right}
            e = E(datafile, p)
            r = e.estimate()
            #print("{}: {}".format(p, r))
            if last_density is not None:
                if r == expected or ((expected - last_density) / (expected - r)) < 0:
                    return {'from': left, 'to': left + window, 'step': 1}
                if direction is not None and direction / (r - last_density) < 0:
                    return {'from': int(left - window/2), 'to': int(left+window/2), 'step': 1}

                direction = r - last_density
            last_density = r
            left = right

