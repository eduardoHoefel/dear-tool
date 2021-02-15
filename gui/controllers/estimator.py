from gui.controllers.window_controller import WindowController
from gui.tools import Menu
from gui.form.controller import FormController

from gui.form.input import Input
from gui.form.select import Select

import estimators.all as estimators
from gui.objects.executable import EstimatorExecutor
from gui.controllers.execution import ExecutionController

from datatypes import nfloat, nint, pfloat

import log

class EstimatorController(WindowController):

    def __init__(self, window_provider):
        title = "Run estimator"
        super().__init__(title, window_provider)

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider, self.remove, self.submit)

        def datafile_options_provider():
            datafiles = self.s.get('datafiles')
            datafile_options = {}

            for d in datafiles:
                datafile_options[d] = d

            return datafile_options

        datafile_select = Select('Datafile', True, datafile_options_provider)

        self.form.add_input('datafile', datafile_select)

        estimator_select = Select('Estimator', True, estimators.get_all)
        self.form.add_input('estimator', estimator_select)

        parameters = {}
        parameters['bins_method'] = Select('Bins method', True, {'manual': "Manual", 'auto': "Auto", 'fd': "Freedman Diacosis", 'doane': "Doane", 'scott': "Scott", 'stone': "Stone", 'rice': "Rice", 'sturges': "Sturges", 'sqrt': "Square root"})
        parameters['bins'] = Input('Bins', False, nint, 9)
        parameters['bin_population'] = Input('Bin population', False, nfloat, 9)
        parameters['kernel'] = Select('Kernel', True, {'gaussian': "Gaussian"})
        parameters['bandwidth'] = Input('Bandwidth', True, pfloat, 0.4)

        for p in parameters.keys():
            self.form.add_input(p, parameters[p])

        def on_estimator_change(old_value, new_value, is_valid=True):
            for inp in parameters.values():
                    inp.disappear()

            if new_value is not None:
                for p in new_value.get_parameters():
                    parameters[p].show()
                    parameters[p].changed()
            pass

        def on_bins_method_change(old_value, new_value, is_valid):
            if new_value == "manual":
                parameters['bins'].reset()
            else:
                parameters['bins'].disable()
                parameters['bins'].set_value("Disabled")

        def on_bins_change(old_value, new_value, is_valid):
            if is_valid:
                datafile = datafile_select.get_value()
                if datafile is not None:
                    samples = datafile.samples
                    parameters['bin_population'].set_value(samples/new_value)

        def on_population_change(old_value, new_value, is_valid):
            if is_valid:
                datafile = datafile_select.get_value()
                if datafile is not None:
                    samples = datafile.samples
                    parameters['bins'].set_value(int(samples/new_value))


        estimator_select.on_change(on_estimator_change)
        parameters['bins_method'].on_change(on_bins_method_change)
        parameters['bins'].on_change(on_bins_change)
        parameters['bin_population'].on_change(on_population_change)
        on_estimator_change(None, None)



    def input(self, key):
        return self.form.input(key)

    def render(self):
        super().render()
        self.form.render()

    def needs_mean(self):
        return self.form.inputs['estimator'] in [KnownFormula, Real]

    def needs_std(self):
        return self.form.inputs['estimator'] in [KnownFormula, Real]

    def submit(self, data):
        datafile = data['datafile']
        Estimator = data['estimator']
        parameters = data

        estimator = Estimator(datafile, parameters)
        execution = EstimatorExecutor(estimator)

        def get_window(title):
            return self.window.internal_renderer.popup(10, 45, 'center', title)

        popup = ExecutionController(get_window, execution)
        WindowController.add(popup)

        pass
