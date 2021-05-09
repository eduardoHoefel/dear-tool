from experiment import Experiment

from datafiles.synthetic import SyntheticDatafile
from calculate import Calculate
import os
os.environ.setdefault('ESCDELAY', '25')
import log

def message(s):
    log.debug(s)
    #print(s)


def temporary():
    log.init()
    seeds = [1234, 1235, 1236, 1237]

    results = {}
    for i, seed in enumerate(seeds):
        message("Running experiment chunk {} of {}".format(i+1, len(seeds)))
        results[seed] = run_experiments(seed)

    results_stats = gather_results_stats(results)
    results_stats = group_by_file_configuration(results_stats)
    organize_stats(results_stats)

    exit()

def run_experiments(seed):

    from estimators.nearest_neighbors import NN
    from estimators.adaptive_histogram import AdaptiveHistogram
    from estimators.histogram import Histogram
    from estimators.kernel import Kernel

    from datafiles.synthetic import SyntheticDatafile
    from datafiles.distribution import norm, uniform, cauchy, dweibull, arcsine

    estimators = [Histogram, AdaptiveHistogram, Kernel, NN]
    dists = [norm, uniform, cauchy, dweibull, arcsine]

    dist_params = [[], [], [], [2.07], []]

    datafile_parameters = [[0, 2, 1500], [0, 5, 1500], [0, 2, 15000], [0, 5, 15000]]

    datafiles = []
    message("Preparing datafiles")
    for pl in datafile_parameters:
        for i, d in enumerate(dists):
            datafile = SyntheticDatafile(d, dist_params[i], *pl, seed=seed)
            datafiles.append(datafile)

    experiments = []
    message("Preparing experiments")
    for d in datafiles:
        for eClass in estimators:
            estimator_parameters = eClass.get_default_experiment_parameters(d)
            exp = Experiment(eClass, d, estimator_parameters)
            experiments.append(exp)

    data = load_experiment(seed)

    next_experiment = data['next_experiment']
    message("Running experiments, starting from experiment {}".format(next_experiment))
    for i, v in enumerate(experiments):
        if i < next_experiment:
            continue

        datafile = str(v.datafile)
        estimator = str(v.EstimatorClass.get_name())

        message("Experiment id: {}".format(i))
        message("\tDatafile: {}".format(datafile))
        message("\tEstimator: {}".format(estimator))

        #print("Preparing...")
        v.prepare()
        #print("Running...")
        v.run_binary_search()

        auto_score, max_score = v.get_auto_score_max_score()
        message("\tResults")
        message("\t\tAuto: {}".format(auto_score))
        message("\t\tMax: {}".format(max_score))

        exp_results = {'id': i, 'datafile': datafile, 'estimator': estimator, 'auto': auto_score, 'max': max_score}
        data['experiments'].append(exp_results)
        data['next_experiment'] = i+1

        write_experiment(seed, data)

    experiments = data['experiments']
    per_file = split_per_file(experiments)
    for f, e in per_file.items():
        per_file[f] = split_per_estimator(f, e)

    return per_file

def split_per_file(experiments):
    per_file = {}
    for e in experiments:
        df = e['datafile']
        file_properties = ",".join(df.split(","))
        if file_properties not in per_file.keys():
            per_file[file_properties] = []

        per_file[file_properties].append(e)

    return per_file

def split_per_estimator(dfile, experiments):

    per_estimator = {}
    for e in experiments:
        est = e['estimator']
        auto_score = e['auto']
        max_score = e['max']

        per_estimator[est] = {}
        per_estimator[est]['auto'] = auto_score
        per_estimator[est]['max'] = max_score

    return per_estimator

def gather_results_stats(results):
    group_per_file = {}
    for seed, results_per_file in results.items():
        for filename, results_per_estimator in results_per_file.items():
            if filename not in group_per_file.keys():
                group_per_file[filename] = []

            group_per_file[filename].append(results_per_estimator)

    stats_per_file = {}
    for filename, results_per_file in group_per_file.items():
        data = {}
        for file_result in results_per_file:
            for est, est_results in file_result.items():
                if est not in data.keys():
                    data[est] = {'auto': [], 'max': []}
                data[est]['auto'].append(est_results['auto'])
                data[est]['max'].append(est_results['max'])

        est_stats = {}
        for est, est_data in data.items():
            est_stats[est] = {}
            est_stats[est]['auto'] = Calculate.stats(est_data['auto'])
            est_stats[est]['max'] = Calculate.stats(est_data['max'])


        stats_per_file[filename] = est_stats
    return stats_per_file

def group_by_file_configuration(stats_per_file):
    file_confs = {}
    for filename, file_stats in stats_per_file.items():
        dist = filename.split(",")[0]
        file_conf = "_".join(filename.split(", ")[1:])
        file_conf = "samples_" + "".join(file_conf.split(" samples"))
        file_conf = str.replace(file_conf, "=", "_")
        if file_conf not in file_confs.keys():
            file_confs[file_conf] = {}
        file_confs[file_conf][dist] = file_stats

    #print(file_confs)
    return file_confs



def organize_stats(results_stats):
    for filename, stats_per_file in results_stats.items():
        #message("Filename: {}".format(filename))
        ests = {}
        for dist, stats_per_dist in stats_per_file.items():
            for est, stats_per_est in stats_per_dist.items():
                if est not in ests.keys():
                    ests[est] = {}
                ests[est][dist] = stats_per_est

        #message(ests)
        write_stats(filename, ests)
            #message("{}_{} = [{}]".format(k2, str.replace(k.lower(), " ", "_"), ", ".join([str(x) for x in v2])))

def write_stats(filename, file_data):
    per_param_est = {'auto': {}, 'max': {}}
    per_est_param = {}

    with open('results/stats/{}.py'.format(filename), 'w') as py_file:
        py_file.write("\n#VARIABLES PER ESTIMATOR\n")
        for est, est_data in file_data.items():
            est_name = est.lower()[0]

            if est not in per_param_est['auto'].keys():
                per_est_param[est_name] = {'auto': {}, 'max': {}}
                per_param_est['auto'][est_name] = {}
                per_param_est['max'][est_name] = {}

            py_file.write("\n#\tVARIABLES FOR {} estimator\n".format(est))
            for dist, dist_data in est_data.items():
                py_file.write("\n#\t\tVARIABLES FOR {} estimator and {} distribution\n".format(est, dist))
                dist_name = "".join([a[0] for a in dist.lower().split(" ")])
                for param_name, param_data in dist_data.items():
                    py_file.write("\n#\t\t\twith {} parameter\n".format(param_name))
                    for stat_name, stat_data in param_data.items():
                        if stat_name not in per_param_est['auto'][est_name].keys():
                            per_est_param[est_name]['auto'][stat_name] = []
                            per_est_param[est_name]['max'][stat_name] = []
                            per_param_est['auto'][est_name][stat_name] = []
                            per_param_est['max'][est_name][stat_name] = []

                        per_param_est[param_name][est_name][stat_name].append(stat_data)
                        per_est_param[est_name][param_name][stat_name].append(stat_data)

                        var_name = "est_data_{}_{}_{}_{}".format(est_name, dist_name, param_name, stat_name)
                        py_file.write("{} = {}\n".format(var_name, str(stat_data)))
                    var_name = "est_data_{}_{}_{}".format(est_name, dist_name, param_name)
                    py_file.write("\n{} = {}\n".format(var_name, str(param_data)))
                var_name = "est_data_{}_{}".format(est_name, dist_name)
                py_file.write("\n{} = {}\n".format(var_name, str(dist_data)))
            var_name = "est_data_{}".format(est_name)
            py_file.write("\n{} = {}\n".format(var_name, str(est_data)))
        py_file.write("\ndata = {}\n".format(str(file_data)))

        py_file.write("\n#VARIABLES PER PARAM ESTIMATOR\n".format(est))
        py_file.write("\nparam_est_data = {}\n".format(str(per_param_est)))

        py_file.write("\n#VARIABLES PER ESTIMATOR PARAM\n".format(est))
        py_file.write("\nest_param_data = {}\n".format(str(per_est_param)))


def load_experiment(seed):
    import json
    try:
        with open('results/experiments/{}.json'.format(seed), 'r') as f:
            data = json.load(f)
    except:
        data = {'next_experiment': 0, 'experiments': []}

    return data

def write_experiment(seed, data):
    import json
    with open('results/experiments/{}.json'.format(seed), 'w') as json_file:
        json.dump(data, json_file)


def main(stdscr):
    from gui.gui import Gui
    log.init()
    Gui(stdscr)

if __name__ == '__main__':
    #temporary()
    from curses import wrapper
    wrapper(main)
