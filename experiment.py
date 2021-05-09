from calculate import Calculate
import scipy as sc

from estimators.known_formula import KnownFormula
import estimators.all as EstimatorsMother

class Experiment():

    def __init__(self, EstimatorClass, datafile, parameters):

        self.parameters = {} if EstimatorClass == 'all' else {k: v for k, v in parameters.items() if k in EstimatorClass.get_parameters()}
        if 'auto' in parameters.keys():
            self.auto = parameters['auto']
        else:
            self.auto = None

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

    def get_estimator_names(self):
        return [e.__class__.get_name() if self.EstimatorClass == 'all' else e.plot_name_short for e in self.estimators.values()]

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
        total = len(self.estimators.keys())
        for i, k in enumerate(self.estimators.keys()):
            #print("Running estimator {} of {}".format(i, total))
            self.run_estimator(k)

    def run_binary_search(self, b0=0, b1=None):
        keys = list(self.estimators.keys())
        if b1 is None:
            b1 = len(keys)-1
        #print("Running binary search between indexes {} and {}".format(b0, b1))

        lc = int((b0+(b0+b1)/2)/2)
        rc = int((b1+(b0+b1)/2)/2)

        rv = self.real_value

        if b1-b0 <= 100:
            #print("running estimators from index {} to {}".format(b0, b1))
            for i in range(b0, b1+1, 1):
                self.run_estimator(keys[i])
                ei = self.estimators[keys[i]].review.estimation
                si = self.estimators[keys[i]].review.score
                #print("id {} had score {} ({} of {})".format(i, si, ei, rv))
        else:
            i0 = keys[lc]
            i1 = keys[rc]
            self.run_estimator(i0)
            self.run_estimator(i1)

            e0 = self.estimators[i0].review.estimation
            s0 = self.estimators[i0].review.score

            e1 = self.estimators[i1].review.estimation
            s1 = self.estimators[i1].review.score

            #print("id {} had score {} ({} of {})".format(lc, s0, e0, rv))
            #print("id {} had score {} ({} of {})".format(rc, s1, e1, rv))

            if (rv > e0 and rv < e1) or (rv < e0 and rv > e1):
                self.run_binary_search(lc, rc)
            elif abs(rv - e0) < abs(rv - e1):
                self.run_binary_search(b0, int((b0+b1)/2))
            else:
                self.run_binary_search(int((b0+b1)/2), b1)

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

    def get_estimator_all_executions(self, EstimatorClass, parameters):
        parameters = {k: v for k, v in parameters.items() if k in EstimatorClass.get_parameters()}
        range_key, range_value, has_more = self.get_range_parameter(parameters)

        estimators = {}

        if range_key is not None:
            from_value = range_value['from']
            to_value = range_value['to']
            step_size = range_value['step']
            steps = round((to_value - from_value)/step_size)+1

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

    def get_auto_score_max_score(self):
        max_score = None
        auto_score = None

        if self.auto is not None:
            self.auto.run()
            self.auto.analyse(self.real_value)
            s = self.auto.review.score
            auto_score = s

        for e in self.estimators.values():
            if auto_score is None and e.auto is True:
                e.run()
                e.analyse(self.real_value)
            if e.output is None:
                continue

            s = e.review.score
            if auto_score is None and e.auto is True:
                auto_score = s

            if max_score is None or s > max_score:
                max_score = s

        return auto_score, max_score



    def get_all_results(self):
        return {k: v.review.estimation for k, v in self.estimators.items()}
    
    def get_name(self):
        import random
        import string
        return self.get_estimator_class_name() + "_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

