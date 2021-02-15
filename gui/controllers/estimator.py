from gui.controllers.window_controller import WindowController
from gui.tools import Menu
from gui.form.controller import FormController

from gui.form.input import Input
from gui.form.select import Select

import estimators.all as estimators
from gui.objects.executable import EstimatorExecutor
from gui.controllers.execution import ExecutionController

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

        self.form.add_input('datafile', Select('Datafile', True, datafile_options_provider))

        estimator_select = Select('Estimator', True, estimators.get_all)
        self.form.add_input('estimator', estimator_select)

        parameters = {}
        parameters['bins'] = Input('Bins', False, int, 9)
        parameters['bin_population'] = Input('Bin population', False, int, 9)

        for p in parameters.keys():
            self.form.add_input(p, parameters[p])



        def on_estimator_change(old_value, new_value):
            for inp in parameters.values():
                    inp.hide()

            if new_value is not None:
                for p in new_value.get_parameters():
                    parameters[p].show()
            pass

        estimator_select.on_change(on_estimator_change)
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
