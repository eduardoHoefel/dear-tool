from gui.form.form_object import FormObject
from gui.window import Line, LineObject
import gui.colors as Colors
from gui.window import Renderer

class DoubleSection(FormObject, CursorManager):

    def __init__(self, section1, section2):
        self.sections = [section1, section2]
        self.init_form_object(section1.default)
        self.cursor = 0

    def set_value(self, value):
        return self.sections[self.cursor].set_value(value)

    def is_focused(self):
        return self.sections[self.cursor].is_focused()

    def focus(self):
        super().focus()
        return self.sections[self.cursor].focus()

    def unfocus(self):
        super().unfocus()
        self.sections[0].unfocus()
        self.sections[1].unfocus()

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
        return self.sections[0].is_valid() and self.sections[1].is_valid

    def on_change(self, on_change_func):
        self.sections[0].on_change(on_change_func)
        self.sections[1].on_change(on_change_func)

    def get_value(self):
        return self.sections[self.cursor].get_value()

    def interactible_cursor_options(self):
        options = {}
        for s in range(self.sections):
            options[s] = self.sections[s]

        return options

    def cursor_input(self, key):
        if key is None:
            return False

        cursor_options = self.interactible_cursor_options()
        current = None if self.cursor is None else cursor_options[self.cursor]

        r = current.input(key)
        if r is True:
            return True

        if key == 'KEY_UP':
            return False
        if key == 'KEY_DOWN':
            return False
        if key == 'KEY_LEFT':
            if self.cursor == 0:
                return False
            self.move_cursor(-1)
            return True
        if key == 'KEY_RIGHT':
            if self.cursor == 1:
                return False
            self.move_cursor(1)
            return True

        return False

    def input(self, key):
        r = self.cursor_input(key)

        return r

    def render(self, renderer):
        separator = "  "

        half_width =  int(renderer_length/2-1.5)
        half_width2 = int(renderer_length/2-1)

        renderers = [Renderer(1, half_width, 0, 0, self.renderer), Renderer(1, half_width2, 0, half_width, self.renderer)]

        self.sections[1-self.cursor].render(renderers[1-self.cursor])
        self.sections[self.cursor].render(renderers[self.cursor])

        return 1
