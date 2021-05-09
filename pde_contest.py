import numpy as np
import estimators.all as EstimatorsMother
from datafiles.synthetic import SyntheticDatafile
from experiment import Experiment
from repeated_experiment import RepeatedExperiment

from datatypes import myfloat

class PDEContest(RepeatedExperiment):

    def __init__(self, EstimatorClass, datafile_parameters, estimator_parameters):
        samples_group = datafile_parameters['samples']

        self.samples_start = samples_group['from']
        self.samples_end = samples_group['to']
        self.samples_steps = samples_group['step']

        self.samples_range = self.samples_end - self.samples_start
        iteractions = int(self.samples_range / self.samples_steps)+1

        super().__init__(iteractions, EstimatorClass, datafile_parameters, estimator_parameters)

    def prepare(self):
        self.experiments = {}
        dist = self.datafile_parameters['dist']
        dist_params = self.datafile_parameters['dist_params']
        loc = self.datafile_parameters['loc']
        scale = self.datafile_parameters['scale']
        samples = self.datafile_parameters['samples']
        original_datafile = SyntheticDatafile(dist, dist_params, loc, scale, samples)

        for i in range(self.iterations):
            samples = self.samples_start + self.samples_steps*i
            datafile = original_datafile.split(samples)

            e = Experiment(self.EstimatorClass, datafile, self.estimator_parameters)
            e.prepare()
            self.experiments[e.get_name()] = e

    def get_samples(self):
        samples = self.datafile_parameters['samples']
        return [self.samples_start + self.samples_steps*i for i in range(self.iterations)]
