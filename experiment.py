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

    def get_estimator_class_name(self):
        return 'All' if self.EstimatorClass == 'all' else self.EstimatorClass.get_name()

    def prepare(self):
        self.estimators = {}
        if self.EstimatorClass == 'all':
            for estimator in EstimatorsMother.get_all():
                #if we are running all estimators, its best to not have fancy parameters
                temp_e = self.get_estimator_all_executions(estimator, {})
                self.estimators[estimator.get_name()] = temp_e[list(temp_e.keys())[0]]
        else:
            self.estimators = self.get_estimator_all_executions(self.EstimatorClass, self.parameters)

    def get_estimator_keys(self):
        return list(self.estimators.keys())
    
    def run_all(self):
        for k in self.estimators.keys():
            self.run_estimator(k)

    def run_estimator(self, key):
        if key not in self.estimators.keys():
            import log
            log.debug(key)
            log.debug(self.estimators.keys())
            exit()
        e = self.estimators[key]
        e.run()
        if self.real_value is not None:
            e.analyse(self.real_value)

        #if key == self.get_estimator_keys()[-1]:
        #    import log
        #    ordered_estimators = sorted(self.get_estimator_keys(), key=lambda k: self.estimators[k].review.estimation)
        #    for i in range(len(ordered_estimators)):
        #        e = ordered_estimators[i]
        #        log.debug("{},\t {},\t {},\t {}".format(i+1, self.estimators[e].bin_population, self.estimators[e].review.score, self.estimators[e].review.estimation))
        #    exit()



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
                    estimators[estimator.id] = estimator

        else:
            estimator = EstimatorClass(self.datafile, parameters)
            estimators[estimator.id] = estimator

        return estimators

    def get_all_scores(self):
        def sorter(item):
            v = self.estimators[item].review.score
            if type(v) == str:
                return 0

            v = 1/v if v > 0 else 1000000
            return v

        ranked_estimators = sorted(self.get_estimator_keys(), key=sorter)


        return {k: self.estimators[k].review.score for k in ranked_estimators}

    def get_all_results(self):
        return {k: v.review.estimation for k, v in self.estimators.items()}
    
    def get_name(self):
        import random
        import string
        return self.get_estimator_class_name() + "_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

