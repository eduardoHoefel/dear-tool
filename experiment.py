from calculate import Calculate
import scipy as sc

from estimators.histogram import Histogram
from estimators.adaptive_histogram import AdaptiveHistogram
from estimators.kernel import Kernel
from estimators.nearest_neighbors import NN
from estimators.real import Real
from estimators.crude import Crude
from estimators.known_formula import KnownFormula

from data_provider import DataProvider

default_estimator_classes = [Real, Crude, Kernel, Histogram, AdaptiveHistogram]

class Experiment():

    def get_e_data(m, s, data):
        e_data = {}

        e_data['m'] = m
        e_data['s'] = s
        e_data['x'] = data
        e_data['f'] = sc.stats.norm.pdf

        return e_data

    def get_estimators(e_data, estimator_classes, custom_attributes={}):

        from collections.abc import Iterable

        estimators = []

        if not isinstance(estimator_classes, Iterable):
            estimator_classes = [estimator_classes]

        for e in estimator_classes:
            if len(custom_attributes) == 0:
                estimators.append(e(e_data))
                continue

            for k in custom_attributes.keys():
                e_data[k] = None
                v1 = custom_attributes[k]

                if not isinstance(v1, Iterable):
                    v1 = [v1]

                for v2 in v1:
                    e_data[k] = v2
                    estimators.append(e(e_data))

                e_data.pop(k)

        return estimators


    def from_real_data(m, s, data, estimator_classes=default_estimator_classes, custom_attributes={}):
        e_data = Experiment.get_e_data(m, s, data)

        estimators = Experiment.get_estimators(e_data, estimator_classes, custom_attributes)

        return Experiment(e_data, estimators)

    def from_syntetic_data(m, s, samples, estimator_classes=default_estimator_classes, custom_attributes={}):
        data = DataProvider.syntetic(m, s, samples)

        return Experiment.from_real_data(m, s, data, estimator_classes, custom_attributes)


    def __init__(self, e_data, estimators):

        self.e_data = e_data
        self.results = {}
        self.estimators = estimators

        self.run()

    def run(self):
        self.expected_result = KnownFormula(self.e_data).estimate()

        for e in self.estimators:
            r = e.estimate()
            self.results[e.name] = r

    def get_results(self):
        return self.results

    def get_errors(self):
        base_r = self.expected_result

        errors = {}
        for k in self.results.keys():
            r = self.results[k]
            errors[k] = Calculate.error(base_r, r)

        return errors

    def get_scores(self, method='auto'):
        base_r = self.expected_result

        scores = {}
        for k in self.results.keys():
            r = self.results[k]
            s = Calculate.score(base_r, r, method)
            if s:
                scores[k] = s

        return scores

    def get_best_estimators(self, top=10):
        errors = self.get_errors()
        best_keys = []

        for i in range(top):
            best_k = None
            for k in errors.keys():
                if k in best_keys:
                    continue

                if best_k is None or errors[k] < errors[best_k]:
                    best_k = k
            if best_k is not None:
                best_keys.append(best_k)

        return best_keys






    def __str__(self):
        max_name_len = 2
        build_str = ''

        build_str += ("Expected:\t\t{}{}\tError (%)\n".format('\t' * (max_name_len-int(len("Expected")/8)), self.expected_result))

        best_keys = self.get_best_estimators()
        for i in range(len(best_keys)):
            name = best_keys[i]
            r = self.results[name]
            build_str += "#{}: H(X) ({}):\t{}{}\t{}\n".format(i+1, name, '\t' * (max_name_len-int(len(name)/8)), r, Calculate.error(self.expected_result, r))

        return build_str

    
