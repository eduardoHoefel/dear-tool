
from estimators.adaptive_histogram import AdaptiveHistogram
from estimators.crude import Crude
from estimators.histogram2 import Histogram2
from estimators.histogram import Histogram
from estimators.kernel import Kernel
from estimators.known_formula import KnownFormula
from estimators.nearest_neighbors import NN
from estimators.real import Real

def get_all():
    estimator_options = {}
    estimator_options[AdaptiveHistogram] = "Adaptive Histogram"
    estimator_options[Crude] = "Crude"
    estimator_options[Histogram2] = "Manual Histogram"
    estimator_options[Histogram] = "Numpy Histogram"
    estimator_options[Kernel] = "Kernel"
    estimator_options[KnownFormula] = "Known Formula"
    estimator_options[NN] = "Nearest Neighbors"
    estimator_options[Real] = "Real"
    
    return estimator_options

def get_name(estimator):
    return get_all()[estimator]
