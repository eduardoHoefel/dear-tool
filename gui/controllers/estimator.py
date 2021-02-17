from gui.controllers.window_controller import WindowController
from gui.tools import Menu
from gui.form.controller import FormController

from gui.form.input import Input
from gui.form.select import Select
from gui.form.section import Section
from gui.form.double_section import DoubleSection
from gui.form.section_break import SectionBreak

import estimators.all as estimators
from executors.executable import EstimatorExecutor
from gui.controllers.execution import ExecutionController

from datatypes import nfloat, nint, pfloat

import log

class EstimatorController(WindowController):

    def __init__(self, window_provider):
        title = "Run estimator"
        super().__init__(title, window_provider)

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider)

        def datafile_options_provider():
            datafiles = self.s.get('datafiles')
            datafile_options = {}

            for d in datafiles:
                datafile_options[d] = d

            return datafile_options

        datafile_select = Section("Datafile", Select(True, datafile_options_provider))

        self.form.add_element('datafile', datafile_select)

        def get_estimator_options():
            keys = estimators.get_all()
            options = {}
            for key in keys:
                options[key] = key.get_name()

            return options


        estimator_select = Section("Estimator", Select(True, get_estimator_options))
        self.form.add_element('estimator', estimator_select)
        self.form.add_element('break1', SectionBreak())

        parameters = estimators.get_all_inputs(datafile_select)
        names = estimators.get_all_input_names()

        for p in parameters.keys():
            self.form.add_element(p, Section(names[p], parameters[p]))

        def on_estimator_change(old_value, new_value, is_valid=True):
            for inp in parameters.values():
                    inp.disappear()

            if new_value is not None:
                for p in new_value.get_parameters():
                    parameters[p].show()
                    parameters[p].reset()
                    parameters[p].changed()

        estimator_select.inp.on_change(on_estimator_change)
        on_estimator_change(None, None)

        cancel = self.form.get_button('cancel', "Cancel", self.remove)
        submit = self.form.get_button('submit', "Submit", self.submit)

        self.form.set_action_button('cancel', cancel)
        self.form.set_action_button('submit', submit)
        self.form.add_element('buttons', DoubleSection(submit, cancel))

        self.form.start()



    def input(self, key):
        return self.form.input(key)

    def render(self):
        super().render()
        self.form.render()

    def submit(self):
        data = self.form.get_data()
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
