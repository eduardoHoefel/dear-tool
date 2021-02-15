from gui.form.form_object import FormObject
from gui.window import Line, LineObject
import gui.colors as Colors

class Input(FormObject):

    def __init__(self, name, required, inp_type, default=None):
        super().__init__()
        self.init_form_object()
        self.name = name
        self.required = required
        self.inp_type = inp_type
        self.default = default
        self.cursor = 0
        self.set_value(default)

    def move_cursor(self, pos):
        rv = self.get_printable_value()
        new_pos = self.cursor + pos
        if new_pos >= len(rv):
            new_pos = len(rv)
        if new_pos < 0:
            new_pos = 0
        self.cursor = new_pos

    def handle_input(self, key):
        if key == 'KEY_LEFT':
            self.move_cursor(+1)
            return True
        if key == 'KEY_RIGHT':
            self.move_cursor(-1)
            return True
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            aux = list(self.value)
            del aux[-(1+self.cursor)]
            self.value = "".join(aux)
            return True
        if key  == 'KEY_DC':
            if self.cursor == 0:
                return False

            aux = list(self.value)
            del aux[-self.cursor]
            self.value = "".join(aux)
            self.cursor -= 1
            return True


        new_value = self.value[:len(self.value) - self.cursor] + key + self.value[len(self.value) - self.cursor:]
        if len(str(new_value)) == 0:
            self.cursor = 0

        self.value = new_value
        return True

    def get_printable_value(self):
        if self.focused:
            return str(self.value)

        return str(self.get_value())

    def set_value(self, value):
        self.value = str(value)

    def get_value(self):
        try:
            return self.inp_type(self.value)
        except:
            return self.value

    def is_valid(self):
        try:
            self.inp_type(self.value)
            return True
        except:
            return False

    def render(self, renderer):
        if not self.visible():
            return self.hidden()

        valid_value = self.is_valid()

        line = Line()

        checked_str = "  " if valid_value else "  "
        required_str = "* " if self.required else "  "
        name_str = "{}: ".format(self.name)
        name_color = Colors.EDITING_VALUE if self.focused else (Colors.VALID_VALUE if valid_value else Colors.DISABLED if not self.enabled else Colors.INVALID_VALUE)
        value_color = Colors.DISABLED if not self.enabled else Colors.INVALID_VALUE if not valid_value else Colors.EDITING_VALUE if self.focused else Colors.DEFAULT
        value_str = self.get_printable_value()

        checked_obj = LineObject(checked_str, 0, {'color': Colors.ERROR})
        required_obj = LineObject(required_str, len(checked_obj), {'color': Colors.IMPORTANT})
        name_obj = LineObject(name_str, len(required_obj), {'color': name_color})

        space_left = renderer.width - len(name_obj)
        padding_length = space_left - len(value_str)
        padding_half = " " *  int(padding_length/2+.5)

        line.add(checked_obj)
        line.add(required_obj)
        line.add(name_obj)

        if self.focused:
            value_p1 = value_str[:len(value_str) - self.cursor]
            value_p2 = value_str[len(value_str) - self.cursor:]

            value_obj1 = LineObject(value_p1, len(padding_half)+len(name_obj), {'color': value_color})
            value_obj2 = LineObject(value_p2, len(value_obj1), {'color': value_color})
            line.add(value_obj2)
            line.add(value_obj1)
        else:
            value_obj = LineObject(value_str, renderer.width - len(value_str), {'color': value_color})
            line.add(value_obj)

        line.render(renderer)

        return True
