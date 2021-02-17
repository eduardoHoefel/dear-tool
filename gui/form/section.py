from gui.form.form_object import FormObject
from gui.window import Line, LineObject
import gui.colors as Colors
from gui.window import Renderer

class Section(FormObject):

    def __init__(self, name, inp):
        self.inp = inp
        self.init_form_object(inp.default)
        self.name = name

    def set_value(self, value):
        return self.inp.set_value(value)

    def is_focused(self):
        return self.inp.is_focused()

    def focus(self):
        return self.inp.focus()

    def unfocus(self):
        return self.inp.unfocus()

    def enable(self):
        return self.inp.enable()

    def disable(self):
        return self.inp.disable()

    def is_enabled(self):
        return self.inp.is_enabled()

    def show(self):
        return self.inp.show()

    def hide(self):
        return self.inp.hide()
    
    def disappear(self):
        return self.inp.disappear()

    def visible(self):
        return self.inp.visible()

    def hidden(self):
        return self.inp.hidden()

    def is_valid(self):
        return self.inp.is_valid()

    def on_change(self, on_change_func):
        pass

    def get_value(self):
        return self.inp.get_value()

    def input(self, key):
        return self.inp.input(key)

    def render(self, renderer):
        if not self.visible():
            return 1 if not self.hidden() else 0

        valid_value = self.is_valid()
        required = self.inp.required

        line = Line()

        checked_str = "  " if valid_value else "  "
        required_str = "* " if required else "  "
        name_str = "{}: ".format(self.name)
        name_color = Colors.EDITING_VALUE if self.is_focused() else (Colors.VALID_VALUE if valid_value else Colors.INVALID_VALUE)

        checked_obj = LineObject(checked_str, 0, {'color': Colors.ERROR})
        required_obj = LineObject(required_str, len(checked_obj), {'color': Colors.IMPORTANT})
        name_obj = LineObject(name_str, len(required_obj), {'color': name_color, 'bold': self.is_focused()})

        line.add(checked_obj)
        line.add(required_obj)
        line.add(name_obj)
        line.render(renderer)

        input_renderer = Renderer(0, -(len(name_obj)), 0, len(name_obj), renderer)
        self.inp.render(input_renderer)

        return 1
