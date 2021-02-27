import numpy as np
import estimators.all as EstimatorsMother
from datafiles.synthetic import SyntheticDatafile
from experiment import Experiment

from datatypes import myfloat

class RepeatedExperiment():

    def __init__(self, iterations, EstimatorClass, datafile_parameters, estimator_parameters):

        self.EstimatorClass = EstimatorClass
        self.experiments = None
        self.iterations = iterations
        self.datafile_parameters = datafile_parameters
        self.estimator_parameters = estimator_parameters
        self.real_value = None

    def prepare(self):
        self.experiments = {}
        m = self.datafile_parameters['m']
        s = self.datafile_parameters['s']
        samples = self.datafile_parameters['samples']

        for i in range(self.iterations):
            datafile = SyntheticDatafile(m, s, samples)
            e = Experiment(self.EstimatorClass, datafile, self.estimator_parameters)
            e.prepare()
            self.experiments[e.get_name()] = e

    def get_estimator_keys(self):
        first_experiment = list(self.experiments.values())[0]
        estimators = first_experiment.get_estimator_keys()
        return estimators

    def get_samples(self):
        samples = self.datafile_parameters['samples']
        return [samples for x in self.experiments.keys()]

    def compute_statistics(self):
        self.real_value = list(self.experiments.values())[0].real_value

        estimators = self.get_estimator_keys()
        self.results = {}
        self.scores = {}
        self.pos = {}
        self.diffs = {}
        self.statistics = {}

        for e in estimators:
            self.results[e] = {}
            self.scores[e] = {}
            self.pos[e] = {}
            self.diffs[e] = {}

        for k, v in self.experiments.items():
            scores = v.get_all_scores()
            results = v.get_all_results()
            key_list = list(scores.keys())
            best_of_the_round = None

            for i in range(len(key_list)):
                key = key_list[i]
                if best_of_the_round is None and type(scores[key]) is not str:
                    best_of_the_round = scores[key]

                self.results[key][k] = results[key]
                self.scores[key][k] = scores[key]
                self.pos[key][k] = len([x for x in scores.values() if type(x) is str or x > scores[key]])+1
                self.diffs[key][k] = 0 if type(scores[key]) is str else best_of_the_round - scores[key]

        for e in estimators:
            e_results = list(self.results[e].values())
            e_scores = list(self.scores[e].values())
            e_pos = list(self.pos[e].values())
            e_diffs = list(self.diffs[e].values())
            s = {}

            s['min_result'] = min(e_results)
            s['max_result'] = max(e_results)
            s['avg_result'] = np.mean(e_results)
            s['std_result'] = np.std(e_results)

            s['min_score'] = min(e_scores)
            s['max_score'] = max(e_scores)
            s['avg_score'] = s['min_score'] if type(s['min_score']) is str else np.mean(e_scores)
            s['std_score'] = s['min_score'] if type(s['min_score']) is str else np.std(e_scores)

            s['min_pos'] = min(e_pos)
            s['max_pos'] = max(e_pos)
            s['avg_pos'] = np.mean(e_pos)
            s['std_pos'] = np.std(e_pos)
            s['score'] = int(1000*(len(e_diffs) - sum(e_diffs)/len(estimators))/(self.iterations))
            if s['score'] < 0:
                import log
                log.debug(e_diffs)
                exit()
            s['pos'] = s['avg_pos']
            s['sample'] = list(self.experiments.values())[0].estimators[e]
            s['name'] = s['sample'].name
            s['participations'] = {k: {'score': v, 'pos': self.pos[e][k]} for k, v in self.scores[e].items()}
            self.statistics[e] = s

    def get_total_steps(self):
        return len(self.get_experiment_keys()) * len(self.get_estimator_keys())

    def get_estimator_keys(self):
        return list(list(self.experiments.values())[0].get_estimator_keys())

    def get_experiment_keys(self):
        return list(self.experiments.keys())

    def run_estimator(self, experiment, estimator):
        self.experiments[experiment].run_estimator(estimator)
