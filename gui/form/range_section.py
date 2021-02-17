from gui.form.form_object import FormObject
from gui.window import Line, LineObject
import gui.colors as Colors
from gui.window import Renderer
from gui.objects.cursors.vlist import VListCursor
from gui.form.double_section import DoubleSection
from gui.form.section import Section
from gui.form.input import Input
from datatypes import pfloat

class RangeSection(FormObject):

    def __init__(self, name, input_from, input_to):
        self.input_from = input_from
        self.input_to = input_to
        self.input_to.value = self.input_to.value
        self.input_step = Input(True, pfloat, 1)

        section_from = Section("From", input_from)
        section_to = Section("To", input_to)

        inputs_section = DoubleSection(section_from, section_to)
        step_section = Section("Steps", self.input_step)
        step_section = DoubleSection(Section(name, None), step_section)

        self.sections = {0: step_section, 1: inputs_section}

        self.cursor = VListCursor(self.sections)
        self.init_form_object(1)

    def set_value(self, value):
        pass

    def unfocus(self):
        super().unfocus()
        self.sections[0].unfocus()
        self.sections[1].unfocus()

    def visible(self):
        return self.input_from.visible() and self.input_to.visible() and self.input_step.visible()

    def focus(self):
        super().focus()

    def enable(self):
        super().enable()
        self.sections[0].enable()
        self.sections[1].enable()

    def disable(self):
        super().disable()
        self.sections[0].disable()
        self.sections[1].disable()

    def show(self):
        super().show()
        self.sections[0].show()
        self.sections[1].show()

    def hide(self):
        super().hide()
        self.sections[0].hide()
        self.sections[1].hide()
    
    def disappear(self):
        super().disappear()
        self.sections[0].disappear()
        self.sections[1].disappear()

    def is_valid(self):
        return self.sections[0].is_valid() and self.sections[1].is_valid()

    def on_change(self, on_change_func):
        pass

    def get_value(self):
        return {'step': self.input_step.get_value(), 'from': self.input_from.get_value(), 'to': self.input_to.get_value()}

    def input(self, key):
        return self.cursor.input(key)

    def render(self, renderer):

        def renderer_provider(index, pos_y, cursor, item):
            if pos_y is None:
                pos_y = 0

            return pos_y, Renderer(1, 0, pos_y, 0, renderer)

        self.cursor.render(renderer_provider)

        return 2
