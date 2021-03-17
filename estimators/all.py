
from estimators.adaptive_histogram import AdaptiveHistogram
from estimators.crude import Crude
from estimators.histogram import Histogram
from estimators.kernel import Kernel
from estimators.known_formula import KnownFormula
from estimators.nearest_neighbors import NN
from estimators.real import Real

from gui.form.input import Input
from gui.form.select import Select
from datatypes import nfloat, nint, pfloat

def get_all():
    return [NN, AdaptiveHistogram, Histogram, Kernel]

def get_all_input_names():
    input_names = {}
    input_names['name'] = "Name"
    input_names['bins_method'] = "Bins Method"
    input_names['bins'] = "Bins"
    input_names['bin_population'] = "Bin Population"
    input_names['population_method'] = "Population Method"
    input_names['kernel'] = "Kernel"
    input_names['bandwidth'] = "Bandwith"
    input_names['result'] = "Result"
    input_names['score'] = "Score"
    input_names['pos'] = "Position"
    input_names['neighbors_method'] = "Neighbors Method"
    input_names['neighbors'] = "Nearest Neighbors"

    return input_names

def get_all_inputs(datafile_select):
    parameters = {}
    parameters['population_method'] = Select(True, {'manual': "Manual", 'auto': "Auto"}, 0)
    parameters['bins_method'] = Select(True, {'manual': "Manual", 'auto': "Auto", 'fd': "Freedman Diacosis", 'doane': "Doane", 'scott': "Scott", 'stone': "Stone", 'rice': "Rice", 'sturges': "Sturges", 'sqrt': "Square root"}, 0)
    parameters['neighbors_method'] = Select(True, {'manual': "Manual", 'auto': "Auto"}, 0)
    parameters['bins'] = Input(False, nint, 9)
    parameters['bin_population'] = Input(False, nfloat, 9)
    parameters['neighbors'] = Input(False, nfloat, 9)
    parameters['kernel'] = Select(True, {'gaussian': "Gaussian"})
    parameters['bandwidth'] = Input(True, pfloat, 0.4)
    
    def on_bins_method_change(old_value, new_value, is_valid):
        if new_value == "manual":
            parameters['bins'].reset()
        else:
            parameters['bins'].disable()
            parameters['bins'].set_value("Disabled")
    
    def on_population_method_change(old_value, new_value, is_valid):
        if new_value == "manual":
            parameters['bin_population'].reset()
        else:
            parameters['bin_population'].disable()
            parameters['bin_population'].set_value("Disabled")
    
    def on_neighbors_method_change(old_value, new_value, is_valid):
        if new_value == "manual":
            parameters['neighbors'].reset()
        else:
            parameters['neighbors'].disable()
            parameters['neighbors'].set_value("Disabled")
    
    
    parameters['bins_method'].on_change(on_bins_method_change)
    parameters['population_method'].on_change(on_population_method_change)
    parameters['neighbors_method'].on_change(on_neighbors_method_change)

    return parameters
