import numpy as np
import estimators.all as EstimatorsMother
from datafiles.syntetic import SynteticDatafile
from experiment import Experiment

class RepeatedExperiment():

    def __init__(self, iterations, EstimatorClass, datafile_parameters, estimator_parameters):

        self.EstimatorClass = EstimatorClass
        self.experiments = None
        self.iterations = iterations
        self.datafile_parameters = datafile_parameters
        self.estimator_parameters = estimator_parameters

    def prepare(self):
        self.experiments = {}
        m = self.datafile_parameters['m']
        s = self.datafile_parameters['s']
        samples = self.datafile_parameters['samples']

        for i in range(self.iterations):
            datafile = SynteticDatafile(m, s, samples)
            e = Experiment(self.EstimatorClass, datafile, self.estimator_parameters)
            e.prepare()
            self.experiments[e.get_name()] = e

    def compute_statistics(self):

        first_experiment = list(self.experiments.values())[0]
        estimators = first_experiment.get_estimator_keys()
        self.scores = {}
        self.pos = {}
        self.statistics = {}

        for e in estimators:
            self.scores[e] = {}
            self.pos[e] = {}

        for k, v in self.experiments.items():
            results = v.get_all_scores()
            key_list = list(results.keys())
            for i in range(len(key_list)):
                key = key_list[i]
                self.scores[key][k] = results[key]
                self.pos[key][k] = i+1

        for e in estimators:
            e_scores = list(self.scores[e].values())
            e_pos = list(self.pos[e].values())
            s = {}

            s['min_score'] = min(e_scores)
            s['max_score'] = max(e_scores)
            s['avg_score'] = np.mean(e_scores)
            s['std_score'] = np.std(e_scores)
            s['min_pos'] = min(e_pos)
            s['max_pos'] = max(e_pos)
            s['avg_pos'] = np.mean(e_pos)
            s['std_pos'] = np.std(e_pos)
            s['score'] = s['avg_score'] / (1+s['std_score'])
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
