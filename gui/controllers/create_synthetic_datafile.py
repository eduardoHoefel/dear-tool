from gui.controllers.window_controller import WindowController
from gui.form.controller import FormController

from gui.form.select import Select
from gui.form.input import Input
from gui.form.section import Section
from gui.form.double_section import DoubleSection
from gui.form.section_break import SectionBreak

from gui.tools import Menu

from estimators.known_formula import KnownFormula
from estimators.real import Real

from datafiles.synthetic import SyntheticDatafile

from datatypes import myfloat, nfloat
from datafiles.distribution import param_map

import log

class CreateSyntheticDatafileController(WindowController):

    def __init__(self, window_provider):
        title = "Create Synthetic Datafile"
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

        self.submitted = False

        cancel = self.form.get_button('cancel', "Cancel", self.remove)
        submit = self.form.get_button('submit', "Submit", self.submit)

        self.form.set_action_button('cancel', cancel)
        self.form.set_action_button('submit', submit)
        self.form.add_element('buttons', DoubleSection(submit, cancel))
        self.form.start()

    def render(self):
        super().render()
        self.form.render()

    def input(self, key):
        self.form.input(key)
        return True

    def submit(self):
        data = self.form.get_data()
        if self.submitted is True:
            return

        self.submitted = True

        dist = data['dist']
        dist_params = [data[x] for x in param_map[dist]]
        loc = data['loc']
        scale = data['scale']
        samples = data['samples']
        datafiles = self.s.get('datafiles')
        if datafiles is None:
            datafiles = []

        seed = self.s.get('seed')
        datafiles.append(SyntheticDatafile(dist, dist_params, loc, scale, samples, seed))
        self.s.set('datafiles', datafiles)
        self.remove()
