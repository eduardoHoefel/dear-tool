from estimators.adaptive import Adaptive
from estimators.histogram import Histogram
from estimators.kernel import Kernel
from estimators.nearest_neighbors import NN
from estimators.real import Real
from estimators.crude import Crude
from estimators.known_formula import KnownFormula

import scipy as sc
import numpy as np

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

def experiment_real_data(m, s, data):

    estimators_data = {}
    estimators_data['m'] = m
    estimators_data['s'] = s
    estimators_data['x'] = data
    estimators_data['f'] = sc.stats.norm.pdf

    results = {}

    estimators = [KnownFormula, Real, Crude, Kernel, Histogram]
    for e in estimators:
        i = e(estimators_data)
        r = i.estimate()
        results[i.name] = r

    return results

def experiment_syntetic_data(m, s, samples):
    syntetic_data = sc.stats.norm.rvs(m, s, samples)

    return experiment_real_data(m, s, syntetic_data)

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
    samples = 50
    data = np.array([-1.82660529, 0.64771807, -4.20509891, -0.74107805, -2.20805863, 2.19241453, -4.02510552, -2.60194738, -2.68046854, -0.8404484, -0.13397538, -3.83246752, 3.95221818, -4.26073647, 1.85597412, -1.15097761, 1.26288319, -2.82723516, -1.63124305, -1.36638109, -2.41201203, -2.18363, -1.43593945, -2.96741991, -2.74393529, -2.04582359, -1.20286753, -1.85056239, -3.11808806, -3.36110253, -0.65306947, -0.61322476, -3.19488784, -1.89293271, 3.80140575, -3.44632189, 0.84791246, 1.5986561, -0.19150187, -1.98013888, -4.19964936, -2.00041118, 1.50903314, -1.80975716, -0.51805535, -2.31350719, -1.85560587, -2.50772003, -5.83904163, -1.9716374])

    results = experiment_real_data(true_mean, true_std_deviation, data)

    max_name_len = 2
    for name in results.keys():
        r = results[name]
        print("H(X) ({}):\t{}{}".format(name, '\t' * (max_name_len-int(len(name)/8)), r))

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

def main():
    single_run()


if __name__ == '__main__':
    main()
