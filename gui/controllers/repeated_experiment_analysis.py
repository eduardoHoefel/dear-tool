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

from datatypes import nfloat, nint, pfloat, pint, myfloat
from datafiles.distribution import param_map

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

        def dist_options_provider():
            from datafiles.distribution import all_distributions
            distributions = {}

            for d in all_distributions:
                distributions[d] = d

            return distributions

        dist_select = Select(True, dist_options_provider)
        dist_section = Section("Distribution", dist_select)

        self.form.add_element('dist', dist_section)
        self.form.add_element('samples', Section("Samples", Input(True, int, 1500)))
        self.form.add_element('break1', SectionBreak())

        all_params = {}

        for dist, params in param_map.items():
            for p in params:
                if p not in all_params.keys():
                    inp = Input(True, myfloat, 1)
                    self.form.add_element(p, Section(p, inp))
                    all_params[p] = inp

        self.form.add_element('break2', SectionBreak())
        self.form.add_element('loc', Section("Mean", Input(True, myfloat, 0)))
        self.form.add_element('scale', Section("Standard deviation", Input(True, nfloat, 2)))

        def on_dist_change(old_value, new_value, is_valid=True):
            for inp in all_params.values():
                    inp.disappear()

            if new_value is not None:
                for p in param_map[new_value]:
                    all_params[p].changed()
                    all_params[p].show()

        dist_select.on_change(on_dist_change)
        on_dist_change(None, None)

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
        range_parameters = ['neighbors', 'bins', 'bin_population', 'bandwidth']
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
        dist = data['dist']
        dist_params = [data[x] for x in param_map[dist]]
        loc = data['loc']
        scale = data['scale']
        samples = data['samples']
        datafile_parameters = {'loc': loc, 'scale': scale, 'samples': samples, 'dist': dist, 'dist_params': dist_params}

        EstimatorClass = data['estimator']
        estimator_parameters = data

        repeated_experiment = RepeatedExperiment(iterations, EstimatorClass, datafile_parameters, estimator_parameters)
        execution = RepeatedExperimentExecutor(repeated_experiment)

        def get_window(title):
            return self.window.internal_renderer.popup(12, 45, 'center', title)

        popup = ExecutionController(get_window, execution)
        WindowController.add(popup)

        pass
