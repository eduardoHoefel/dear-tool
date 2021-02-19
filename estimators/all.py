
from estimators.adaptive_histogram import AdaptiveHistogram
from estimators.crude import Crude
from estimators.histogram2 import Histogram2
from estimators.histogram import Histogram
from estimators.kernel import Kernel
from estimators.known_formula import KnownFormula
from estimators.nearest_neighbors import NN
from estimators.real import Real

from gui.form.input import Input
from gui.form.select import Select
from datatypes import nfloat, nint, pfloat

def get_all():
    return [AdaptiveHistogram, Crude, Histogram2, Histogram, Kernel, KnownFormula, NN, Real]

def get_all_input_names():
    input_names = {}
    input_names['name'] = "Name"
    input_names['bins_method'] = "Bins Method"
    input_names['bins'] = "Bins"
    input_names['bin_population'] = "Bin Population"
    input_names['kernel'] = "Kernel"
    input_names['bandwidth'] = "Bandwith"
    input_names['result'] = "Result"
    input_names['score'] = "Score"

    return input_names

def get_all_inputs(datafile_select):
    parameters = {}
    parameters['bins_method'] = Select(True, {'manual': "Manual", 'auto': "Auto", 'fd': "Freedman Diacosis", 'doane': "Doane", 'scott': "Scott", 'stone': "Stone", 'rice': "Rice", 'sturges': "Sturges", 'sqrt': "Square root"}, 0)
    parameters['bins'] = Input(False, nint, 9)
    parameters['bin_population'] = Input(False, nfloat, 9)
    parameters['kernel'] = Select(True, {'gaussian': "Gaussian"})
    parameters['bandwidth'] = Input(True, pfloat, 0.4)
    
    def on_bins_method_change(old_value, new_value, is_valid):
        if new_value == "manual":
            parameters['bins'].reset()
        else:
            parameters['bins'].disable()
            parameters['bins'].set_value("Disabled")
    
    #if datafile_select is not None:
    #   def on_bins_change(old_value, new_value, is_valid):
    #       if is_valid:
    #           datafile = datafile_select.get_value()
    #           if datafile is not None:
    #               samples = datafile.samples
    #               parameters['bin_population'].set_value(samples/new_value)
    #   
    #   def on_population_change(old_value, new_value, is_valid):
    #       if is_valid:
    #           datafile = datafile_select.get_value()
    #           if datafile is not None:
    #               samples = datafile.samples
    #               parameters['bins'].set_value(int(samples/new_value))
    #   parameters['bins'].on_change(on_bins_change)
    #   parameters['bin_population'].on_change(on_population_change)
    
    
    parameters['bins_method'].on_change(on_bins_method_change)

    return parameters
