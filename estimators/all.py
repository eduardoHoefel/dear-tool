
from estimators.adaptive_histogram import AdaptiveHistogram
from estimators.crude import Crude
from estimators.histogram2 import Histogram2
from estimators.histogram import Histogram
from estimators.kernel import Kernel
from estimators.known_formula import KnownFormula
from estimators.nearest_neighbors import NN
from estimators.real import Real

def get_all():
    return [AdaptiveHistogram, Crude, Histogram2, Histogram, Kernel, KnownFormula, NN, Real]
