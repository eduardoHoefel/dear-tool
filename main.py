from experiment import Experiment
from statistics import Statistics

import scipy as sc
import numpy as np

from estimators.adaptive_histogram import AdaptiveHistogram

"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter #for counting elements in a histogram
from scipy.stats.kde import gaussian_kde
import statsmodels.api as sm
from statsmodels.nonparametric.bandwidths import bw_silverman, bw_scott, select_bandwidth
from IPython.display import display
from scipy.integrate import quad
from scipy.stats import norm, entropy
from scipy.stats import rayleigh
from scipy.stats import binom
import seaborn as sns
import scipy.stats as ss
from sklearn.neighbors import KernelDensity
"""

def experiment_precision(m, s, min_points, max_points):
    columns = 10
    step = 1000#int((max_points - min_points)/columns)
    samples = list(range(min_points, max_points, step))

    r_list = {}

    for i,value in enumerate(samples):
        result = experiment_syntetic_data(m, s, value)
        for j in result.keys():
            if j not in r_list:
                r_list[j] = []

            r_list[j].append(result[j])

    return samples, r_list

def single_run():
    true_mean = -2
    true_std_deviation = 2
    samples = 10000

    #results = experiment(true_mean, true_std_deviation, data)
    def f():
        e = Experiment.from_syntetic_data(true_mean, true_std_deviation, samples, AdaptiveHistogram, {'bins': range(1, int(samples/2)), 'bin_population': range(1, int(samples/2))})

        return e.get_scores(method='log2')

    s = Statistics(100, f)

    print(s)

def precision_run():
    import matplotlib.pyplot as plt

    true_mean = -2
    true_std_deviation = 2
    min_samples = 50
    max_samples = 10000

    samples, results = experiment_precision(true_mean, true_std_deviation, min_samples, max_samples)

    print(results)

    for x in results.keys():
        plt.plot(samples, results[x], label=x)

    plt.xlabel('Number of samples used for estimation')
    plt.ylabel('Estimated entropy values')
    plt.legend()
    plt.show();

def main(stdscr):
    from gui.gui import Gui
    Gui(stdscr)


if __name__ == '__main__':
    from curses import wrapper
    wrapper(main)
