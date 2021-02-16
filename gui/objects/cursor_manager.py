
class CursorManager():

    def interactible_cursor_options(self):
        return {}

    def move_cursor(self, pos):
        cursor_options = self.interactible_cursor_options()
        cursor_values = list(cursor_options.keys())

        cur_pos = cursor_values.index(self.cursor)
        new_pos = cur_pos + pos

        cursor_options[self.cursor].unfocus()
        self.cursor = cursor_values[new_pos % len(cursor_values)]
        cursor_options[self.cursor].focus()

    def cursor_input(self, key):
        if key is None:
            return False

        cursor_options = self.interactible_cursor_options()
        current = None if self.cursor is None else cursor_options[self.cursor]

        r = current.input(key)
        if r is True:
            return True

        if key == 'KEY_UP':
            self.move_cursor(-1)
            return True
        if key == 'KEY_DOWN':
            self.move_cursor(1)
            return True
        if key == 'KEY_LEFT':
            self.move_cursor(-1)
            return True
        if key == 'KEY_RIGHT':
            self.move_cursor(1)
            return True

        return False
