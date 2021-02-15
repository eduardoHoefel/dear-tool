from gui.controllers.window_controller import WindowController
from gui.form.controller import FormController
from gui.form.input import Input
from gui.tools import Menu

from estimators.known_formula import KnownFormula
from estimators.real import Real

from datafiles.syntetic import SynteticDatafile

from datatypes.positive_float import pfloat

import log

class CreateSynteticDatafileController(WindowController):

    def __init__(self, window_provider):
        title = "Create Syntetic Datafile:"
        super().__init__(title, window_provider)

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider, self.remove, self.submit)
        self.form.add_input('samples', Input('Samples', True, int, 1500))
        self.form.add_input('m', Input('Mean', True, float, -2))
        self.form.add_input('s', Input('Standard deviation', True, pfloat, 2))

        self.submitted = False

    def render(self):
        super().render()
        self.form.render()

    def input(self, key):
        self.form.input(key)
        return True

    def submit(self, data):
        if self.submitted is True:
            return

        self.submitted = True

        m = data['m']
        s = data['s']
        samples = data['samples']
        datafiles = self.s.get('datafiles')
        if datafiles is None:
            datafiles = []

        datafiles.append(SynteticDatafile(m, s, samples))
        self.s.set('datafiles', datafiles)
        self.remove()
