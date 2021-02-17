from calculate import Calculate
import scipy as sc

from estimators.known_formula import KnownFormula
import estimators.all as EstimatorsMother

class Experiment():

    def __init__(self, EstimatorClass, datafile, parameters):

        self.parameters = {} if EstimatorClass == 'all' else {k: v for k, v in parameters.items() if k in EstimatorClass.get_parameters()}
        self.datafile = datafile
        self.results = {}
        self.EstimatorClass = EstimatorClass
        self.estimators = None

        self.real_value = datafile.density

    def get_range_parameter(self, parameters):
        found_k = None
        found_v = None

        if parameters is None:
            return None, None, None

        for k,v in parameters.items():
            if type(v) is dict:
                if found_k is not None:
                    return found_k, found_v, True
                found_k = k
                found_v = v

        return found_k, found_v, False

    def prepare(self):
        self.estimators = {}
        if self.EstimatorClass == 'all':
            for estimator in EstimatorsMother.get_all():
                #if we are running all estimators, its best to not have fancy parameters
                self.estimators.update(self.get_estimator_all_executions(estimator, {}))
        else:
            self.estimators = self.get_estimator_all_executions(self.EstimatorClass, self.parameters)

    def get_estimator_keys(self):
        return list(self.estimators.keys())

    def run_estimator(self, key):
        e = self.estimators[key]
        e.run()
        if self.real_value is not None:
            e.analyse(self.real_value)


    def get_estimator_all_executions(self, EstimatorClass, parameters):
        parameters = {k: v for k, v in parameters.items() if k in EstimatorClass.get_parameters()}
        range_key, range_value, has_more = self.get_range_parameter(parameters)

        estimators = {}

        if range_key is not None:
            from_value = range_value['from']
            to_value = range_value['to']
            step_size = range_value['step']
            steps = round((to_value - from_value)/step_size)

            p2 = {k: v for k, v in parameters.items() if v != range_value}
            for i in range(steps):
                v = i*step_size + from_value
                p2[range_key] = v
                if has_more is True:
                    estimators.update(self.get_estimator_all_executions(EstimatorClass, p2))
                else:
                    estimator = EstimatorClass(self.datafile, p2)
                    estimators[estimator.name] = estimator

        else:
            estimator = EstimatorClass(self.datafile, parameters)
            estimators[estimator.name] = estimator

        return estimators
