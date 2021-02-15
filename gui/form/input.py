from gui.form.form_object import FormObject

class Input(FormObject):

    def __init__(self, name, required, inp_type, default=None):
        super().__init__()
        self.init_form_object()
        self.name = name
        self.required = required
        self.inp_type = inp_type
        self.default = default
        self.value = str(default)
        self.cursor = 0

    def move_cursor(self, pos):
        rv = self.get_renderable_value()
        new_pos = self.cursor + pos
        if new_pos >= len(rv):
            new_pos = len(rv)
        if new_pos < 0:
            new_pos = 0
        self.cursor = new_pos

    def input(self, key):
        if key == 'KEY_LEFT':
            self.move_cursor(+1)
            return True
        if key == 'KEY_RIGHT':
            self.move_cursor(-1)
            return True
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            self.value = self.value[:-1]
            return True

        newvalue = self.value[:len(self.value) - self.cursor] + key + self.value[len(self.value) - self.cursor:]
        self.value = newvalue
        return True

    def get_renderable_value(self):
        if self.focused:
            return self.value

        return str(self.get_value())

    def get_value(self):
        try:
            return self.inp_type(self.value)
        except:
            return self.default

    def is_valid(self):
        try:
            self.inp_type(self.value)
            return True
        except:
            return False

    def render(self, renderer):
        if not self.visible():
            return self.hidden()

        if self.is_valid():
            checked_str = " "
        else:
            checked_str = "×"

        value_str = self.get_renderable_value()

        required_str = "*" if self.required else " "

        left_part = "{} {}{}: ".format(checked_str, required_str, self.name)


        if self.focused:
            right_part_1 = value_str[:len(value_str)-self.cursor]
            right_part_2 = value_str[len(value_str)-self.cursor:]

            left_part += right_part_1
            renderer.addstr(0, len(left_part), right_part_2)
            renderer.addstr(0, 0, left_part)
        else:
            padding = " " * (renderer.width - len(left_part) - len(value_str) - 1)
            right_part = padding + value_str

            renderer.addstr(0, 0, left_part + right_part)

        return True
