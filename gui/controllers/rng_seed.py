from gui.controllers.window_controller import WindowController
from gui.form.controller import FormController

from gui.form.input import Input
from gui.form.section import Section
from gui.form.double_section import DoubleSection
from gui.form.section_break import SectionBreak

from gui.tools import Menu

from estimators.known_formula import KnownFormula
from estimators.real import Real

from datatypes import nonenint

import log

class RNGSeedController(WindowController):

    def __init__(self, window_provider):
        title = "Set RNG seed"
        super().__init__(title, window_provider)

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider)

        seed = self.s.get('seed')
        if seed is None:
            seed = ''

        self.form.add_element('seed', Section("Seed", Input(True, nonenint, seed)))

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

        seed = data['seed']
        self.s.set('seed', seed)
        self.remove()
