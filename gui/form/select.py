from gui.form.form_object import FormObject
from gui.window import Line, LineObject
import gui.colors as Colors

class Select(FormObject):

    def __init__(self, required, options, default=None):
        self.init_form_object(default)
        self.required = required

        if type(options) == dict:
            def options_provider():
                return options

            self.options_provider = options_provider
        else:
            self.options_provider = options

        self.going_right = True

    def set_value(self, value):
        import log
        if value is not None and type(value) != int:
            log.debug(value)
            exit()
        self.cursor = value

    def move_cursor(self, pos):
        option_dict = self.options_provider()
        if len(option_dict.keys()) == 0:
            return False

        if pos is None:
            self.cursor = None
            self.going_right = True
            return True

        if self.cursor is None:
            if pos > 0:
                self.cursor = 0
                self.going_right = len(option_dict.keys()) > 1
                return True
            return False

        new_pos = self.cursor + pos
        self.going_right = (new_pos > self.cursor)

        if new_pos >= len(option_dict.keys())-1:
            new_pos = len(option_dict.keys())-1
            self.going_right = False

        if new_pos < 0:
            new_pos = None
            self.going_right = True

        self.cursor = new_pos
        return True

    def handle_input(self, key):
        if not self.enabled:
            return False

        if key == 'KEY_LEFT':
            return self.move_cursor(-1)
        if key == 'KEY_RIGHT':
            return self.move_cursor(+1)
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
            return 1 if not self.hidden() else 0

        option_dict = self.options_provider()
        valid_value = self.is_valid()

        line = Line()

        cursor_placer = LineObject("", 0, None)

        value_color = Colors.DISABLED if not self.enabled else Colors.INVALID_VALUE if not valid_value else Colors.EDITING_VALUE if self.focused else Colors.DEFAULT
        value_str = str(self.get_printable_value())
        left_symbol = "<" if self.enabled and self.cursor is not None else " "
        right_symbol = ">" if self.enabled and len(option_dict.keys()) > 0 and (self.cursor is None or self.cursor < (len(option_dict.keys())-1)) else " "

        padding_length = renderer.width - len(value_str)
        padding_half = " " *  int(padding_length/2-.5)
        padding_half2 = " " * int(padding_length/2-1)

        if self.focused:
            left_symbol_obj = LineObject(left_symbol, len(cursor_placer), {'color': Colors.PRESSABLE})
            value_obj = LineObject(padding_half+value_str+padding_half2, len(left_symbol_obj), {'color': value_color})
            right_symbol_obj = LineObject(right_symbol, len(value_obj), {'color': Colors.PRESSABLE})

            if self.going_right:
                line.add(cursor_placer)
                line.add(left_symbol_obj)
                line.add(right_symbol_obj)
                line.add(value_obj)
            else:
                line.add(right_symbol_obj)
                line.add(value_obj)
                line.add(left_symbol_obj)
                line.add(cursor_placer)
        else:
            value_obj = LineObject(value_str, renderer.width - len(value_str), {'color': value_color})
            line.add(value_obj)

        line.render(renderer)

        return 1
