from gui.form.form_object import FormObject
from gui.window import Line, LineObject
import gui.colors as Colors
import gui.objects.keys as Keys

class Input(FormObject):

    def __init__(self, required, inp_type, default=None):
        self.init_form_object(default)
        self.required = required
        self.inp_type = inp_type
        self.cursor = 0
        self.reset()

    def move_cursor(self, pos):
        rv = self.get_printable_value()
        new_pos = self.cursor + pos
        if new_pos >= len(rv):
            new_pos = len(rv)
        if new_pos < 0:
            new_pos = 0

        r = self.cursor != new_pos
        self.cursor = new_pos
        return r

    def handle_input(self, key):
        if key is None:
            return False

        if key in Keys.INPUT_IGNORE:
            return False

        if key == Keys.LEFT:
            return self.move_cursor(+1)

        if key == Keys.RIGHT:
            return self.move_cursor(-1)

        if key in Keys.BACKSPACE:
            if self.cursor == len(self.value):
                return False

            aux = list(self.value)
            del aux[-(1+self.cursor)]
            self.value = "".join(aux)
            return True
        if key == Keys.DELETE:
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
            return 1 if not self.hidden() else 0

        valid_value = self.is_valid()

        line = Line()

        value_color = Colors.DISABLED if not self.enabled else Colors.INVALID_VALUE if not valid_value else Colors.EDITING_VALUE if self.focused else Colors.DEFAULT
        value_str = self.get_printable_value()

        padding_length = renderer.width - len(value_str)
        padding_half = " " *  int(padding_length/2+.5)

        if self.focused:
            value_p1 = value_str[:len(value_str) - self.cursor]
            value_p2 = value_str[len(value_str) - self.cursor:]

            value_obj1 = LineObject(value_p1, len(padding_half), {'color': value_color})
            value_obj2 = LineObject(value_p2, len(value_obj1), {'color': value_color})
            line.add(value_obj2)
            line.add(value_obj1)
        else:
            value_obj = LineObject(value_str, renderer.width - len(value_str), {'color': value_color})
            line.add(value_obj)

        line.render(renderer)

        return 1
