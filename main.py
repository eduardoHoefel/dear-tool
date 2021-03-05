import log
from gui.gui import Gui

from datafiles.synthetic import SyntheticDatafile
import os
os.environ.setdefault('ESCDELAY', '25')


def main(stdscr):
    log.init()
    Gui(stdscr)

def temporary():
    from repeated_experiment import RepeatedExperiment
    from estimators.nearest_neighbors import NN
    from datafiles.synthetic import SyntheticDatafile
    import operator

    tests = []
    for s in [10]:
        for samples in [300, 500, 800, 1300, 2100, 3400, 5500, 8900, 14400, 23300, 37700, 61000, 98700, 159700, 258400]:
            datafile = SyntheticDatafile(-2, s, samples)
            neighbors_range = NN.get_parameter_range(NN, 'neighbors', datafile, 30)

            datafile_parameters = {'m': -2, 's': s, 'samples': samples}
            estimator_parameters = {'neighbors': neighbors_range}
            r = RepeatedExperiment(100, NN, datafile_parameters, estimator_parameters)
            r.prepare()
            r.run_all()
            r.compute_statistics()
            sts = {k: v['score'] for k, v in r.statistics.items()}
            best_key = max(sts.items(), key=operator.itemgetter(1))[0]
            first_experiment = list(r.experiments.values())[0]
            best_n = first_experiment.estimators[best_key].neighbors
            line = "table[{}][{}] = {}".format(s, samples, best_n)
            tests.append(line)
            print(line)

    import log
    for line in tests:
        log.debug(line)

if __name__ == '__main__':
    from curses import wrapper
    #temporary()
    wrapper(main)
