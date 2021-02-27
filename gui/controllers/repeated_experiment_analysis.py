from gui.controllers.window_controller import WindowController
from gui.tools import Menu
from gui.form.controller import FormController

from gui.form.input import Input
from gui.form.select import Select
from gui.form.section import Section
from gui.form.range_section import RangeSection
from gui.form.double_section import DoubleSection
from gui.form.section_break import SectionBreak

import estimators.all as Estimators

from repeated_experiment import RepeatedExperiment
from executors.executable import RepeatedExperimentExecutor
from gui.controllers.execution import ExecutionController

from datatypes import nfloat, nint, pfloat, pint

import log

class RepeatedExperimentAnalysisController(WindowController):

    def __init__(self, window_provider):
        title = "Run repeated experiment"
        super().__init__(title, window_provider)

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider)

        iterations_input = Section("Iterations", Input(True, pint, 100))
        self.form.add_element('iterations', iterations_input)
        self.form.add_element('break1', SectionBreak())

        samples_input = Section("Synthetic samples", Input(True, pint, 1000))

        self.form.add_element('samples', samples_input)

        mean_input = Section("Mean", Input(True, float, -2))
        self.form.add_element('mean', mean_input)

        std_input = Section("Standant deviation", Input(True, pint, 2))
        self.form.add_element('std', std_input)
        self.form.add_element('break2', SectionBreak())

        def get_estimator_options():
            keys = Estimators.get_all()
            options = {}
            for key in keys:
                options[key] = key.get_name()

            options['all'] = "All"

            return options


        estimator_select = Section("Estimator", Select(True, get_estimator_options))
        self.form.add_element('estimator', estimator_select)
        self.form.add_element('break3', SectionBreak())

        min_parameters = Estimators.get_all_inputs(None)
        max_parameters = Estimators.get_all_inputs(None)
        names = Estimators.get_all_input_names()

        simple_parameters = ['bins_method', 'kernel']
        range_parameters = ['bins', 'bin_population', 'bandwidth']
        for p in simple_parameters:
            self.form.add_element(p, Section(names[p], min_parameters[p]))

        for p in range_parameters:
            self.form.add_element(p, RangeSection(names[p], min_parameters[p], max_parameters[p]))

        def on_estimator_change(old_value, new_value, is_valid=True):
            for inp in min_parameters.values():
                    inp.disappear()
            for inp in max_parameters.values():
                    inp.disappear()

            if new_value is not None and type(new_value) != str:
                for p in new_value.get_parameters():
                    min_parameters[p].show()
                    min_parameters[p].reset()
                    min_parameters[p].changed()
                    max_parameters[p].show()
                    max_parameters[p].reset()
                    cur_value = max_parameters[p].get_value()

                    if type(cur_value) != str and cur_value is not None:
                        max_parameters[p].set_value(cur_value*100)
                    max_parameters[p].changed()

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

        iterations = data['iterations']
        m = data['mean']
        s = data['std']
        samples = data['samples']
        datafile_parameters = {'m': m, 's': s, 'samples': samples}

        EstimatorClass = data['estimator']
        estimator_parameters = data

        repeated_experiment = RepeatedExperiment(iterations, EstimatorClass, datafile_parameters, estimator_parameters)
        execution = RepeatedExperimentExecutor(repeated_experiment)

        def get_window(title):
            return self.window.internal_renderer.popup(12, 45, 'center', title)

        popup = ExecutionController(get_window, execution)
        WindowController.add(popup)

        pass
