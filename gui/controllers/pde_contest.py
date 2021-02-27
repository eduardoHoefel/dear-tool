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

import log

class PDEContestController(WindowController):

    def __init__(self, window_provider):
        title = "Probability Density Estimators contest"
        super().__init__(title, window_provider)

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider)

        self.form.add_element('samples', RangeSection('Synthetic samples', Input(True, pint, 1000), Input(True, pint, 10000)))

        mean_input = Section("Mean", Input(True, float, -2))
        self.form.add_element('mean', mean_input)

        std_input = Section("Standant deviation", Input(True, pint, 2))
        self.form.add_element('std', std_input)
        self.form.add_element('break2', SectionBreak())

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
        m = data['mean']
        s = data['std']
        datafile_parameters = {'m': m, 's': s, 'samples': samples}

        EstimatorClass = data['estimator']
        estimator_parameters = data

        pde_contest = PDEContest(EstimatorClass, datafile_parameters, estimator_parameters)
        execution = RepeatedExperimentExecutor(pde_contest)

        def get_window(title):
            return self.window.internal_renderer.popup(12, 45, 'center', title)

        popup = ExecutionController(get_window, execution)
        WindowController.add(popup)
