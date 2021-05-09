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

from pde_contest import PDEContest
from executors.executable import RepeatedExperimentExecutor
from gui.controllers.execution import ExecutionController

from datatypes import nfloat, nint, pfloat, pint
from datafiles.distribution import param_map

import log

class PDEContestController(WindowController):

    def __init__(self, window_provider):
        title = "Probability Density Estimators contest"
        super().__init__(title, window_provider)

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider)

        def dist_options_provider():
            from datafiles.distribution import all_distributions
            distributions = {}

            for d in all_distributions:
                distributions[d] = d

            return distributions

        dist_select = Select(True, dist_options_provider)
        dist_section = Section("Distribution", dist_select)

        self.form.add_element('dist', dist_section)
        self.form.add_element('samples', RangeSection('Samples', Input(True, pint, 1000), Input(True, pint, 10000)))
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

        estimator_select = Section("Estimator", Select(True, {'all': "All"}, 0))
        self.form.add_element('estimator', estimator_select)
        self.form.add_element('break3', SectionBreak())

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

        samples = data['samples']
        dist = data['dist']
        dist_params = [data[x] for x in param_map[dist]]
        loc = data['loc']
        scale = data['scale']
        samples = data['samples']
        datafile_parameters = {'loc': loc, 'scale': scale, 'samples': samples, 'dist': dist, 'dist_params': dist_params}

        EstimatorClass = data['estimator']
        estimator_parameters = data

        pde_contest = PDEContest(EstimatorClass, datafile_parameters, estimator_parameters)
        execution = RepeatedExperimentExecutor(pde_contest)

        def get_window(title):
            return self.window.internal_renderer.popup(12, 45, 'center', title)

        popup = ExecutionController(get_window, execution)
        WindowController.add(popup)
