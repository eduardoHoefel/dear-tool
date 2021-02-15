from gui.form.form_object import FormObject

class Select(FormObject):

    def __init__(self, name, required, options_provider, default=None):
        super().__init__()
        self.init_form_object()
        self.name = name
        self.required = required
        self.default = default
        self.cursor = default
        self.options_provider = options_provider
        self.going_right = True

    def move_cursor(self, pos):
        option_dict = self.options_provider()
        if len(option_dict.keys()) == 0:
            return

        if pos is None:
            self.cursor = None
            self.going_right = True
            return

        if self.cursor is None:
            if pos > 0:
                self.cursor = 0
                self.going_right = True

            return

        new_pos = self.cursor + pos
        self.going_right = (new_pos > self.cursor)

        if new_pos >= len(option_dict.keys())-1:
            new_pos = len(option_dict.keys())-1
            self.going_right = False

        if new_pos < 0:
            new_pos = None
            self.going_right = True

        self.cursor = new_pos

    def input(self, key):
        if key == 'KEY_LEFT':
            self.move_cursor(-1)
            return True
        if key == 'KEY_RIGHT':
            self.move_cursor(+1)
            return True
        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            self.move_cursor(None)
            return True

        return False

    def get_value(self):
        if self.cursor is None:
            return None

        option_dict = self.options_provider()
        return list(option_dict.keys())[self.cursor]

    def get_printable_value(self):
        if self.cursor is None:
            return None

        option_dict = self.options_provider()
        return option_dict[list(option_dict.keys())[self.cursor]]


    def is_valid(self):
        if self.cursor is None and self.required is True:
            return False

        return True

    def render(self, renderer):
        if not self.visible():
            return self.hidden()

        option_dict = self.options_provider()

        if self.is_valid():
            checked_str = " "
        else:
            checked_str = "×"

        value_str = str(self.get_printable_value())

        required_str = "*" if self.required else " "

        left_part = "{} {}{}: ".format(checked_str, required_str, self.name)


        if self.focused:
            left_symbol = "<" if self.cursor is not None else " "
            right_symbol = ">" if len(option_dict.keys()) > 0 and (self.cursor is None or self.cursor < (len(option_dict.keys())-1)) else " "

            padding_length = (renderer.width - len(left_part) - len(value_str) - 2)
            padding_half = " " * int(padding_length/2)
            padding_half2 = " " * int((padding_length+1)/2)

            if self.going_right:
                right_part_1 = "{}{}{}{}".format(left_symbol, padding_half, value_str, padding_half2)
                right_part_2 = right_symbol

                left_part += right_part_1
                renderer.addstr(0, len(left_part), right_part_2)
                renderer.addstr(0, 0, left_part)
            else:
                right_part = "{}{}{}{}{}".format(left_symbol, padding_half, value_str, padding_half2, right_symbol)

                renderer.addstr(0, len(left_part), right_part)
                renderer.addstr(0, 0, left_part)
        else:
            padding = " " * (renderer.width - len(left_part) - len(value_str) - 1)
            right_part = padding + value_str

            renderer.addstr(0, 0, left_part + right_part)

        return True
