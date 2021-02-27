from gui.controllers.window_controller import WindowController
from gui.tools import Menu
from gui.form.controller import FormController

from gui.form.select import Select
from gui.form.section import Section
from gui.form.double_section import DoubleSection
from gui.form.section_break import SectionBreak

import estimators.all as Estimators

import log

class PlotController(WindowController):

    def __init__(self, window_provider, data_controller):
        title = "Plot data"
        super().__init__(title, window_provider)

        self.data_controller = data_controller

        def window_provider(title):
            return self.window.internal_renderer

        self.form = FormController(window_provider)

        def datafile_options_provider():
            datafiles = self.s.get('datafiles')
            datafile_options = {}

            for d in datafiles:
                datafile_options[d] = d

            return datafile_options

        x_axis = Section("X Axis", Select(True, data_controller.get_x_axis_options()))
        self.form.add_element('x', x_axis)

        y_axis = Section("Y Axis", Select(True, data_controller.get_y_axis_options()))
        self.form.add_element('y', y_axis)

        style = Section("Style", Select(True, {'lines': 'Lines', 'dots': "Dots", 'bars': "Bars"}))
        self.form.add_element('style', style)

        cancel = self.form.get_button('cancel', "Cancel", self.remove)
        submit = self.form.get_button('submit', "Plot", self.submit)

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
        x = data['x']
        y = data['y']
        style = data['style']
        self.data_controller.plot(x, y, style)
