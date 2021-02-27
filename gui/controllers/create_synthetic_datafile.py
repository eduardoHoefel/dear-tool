from gui.controllers.window_controller import WindowController
from gui.form.controller import FormController

from gui.form.input import Input
from gui.form.section import Section
from gui.form.double_section import DoubleSection
from gui.form.section_break import SectionBreak

from gui.tools import Menu

from estimators.known_formula import KnownFormula
from estimators.real import Real

from datafiles.synthetic import SyntheticDatafile

from datatypes import myfloat, nfloat

import log

class CreateSyntheticDatafileController(WindowController):

    def __init__(self, window_provider):
        title = "Create Synthetic Datafile"
        super().__init__(title, window_provider)

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider)

        self.form.add_element('samples', Section("Samples", Input(True, int, 1500)))
        self.form.add_element('m', Section("Mean", Input(True, myfloat, -2)))
        self.form.add_element('s', Section("Standard deviation", Input(True, nfloat, 2)))

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

        m = data['m']
        s = data['s']
        samples = data['samples']
        datafiles = self.s.get('datafiles')
        if datafiles is None:
            datafiles = []

        datafiles.append(SyntheticDatafile(m, s, samples))
        self.s.set('datafiles', datafiles)
        self.remove()
