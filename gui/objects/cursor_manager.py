
class CursorManager():

    def cursor_values(self):
        return []

    def cursor_options(self):
        return {}

    def move_cursor(self, pos):
        cursor_values = self.cursor_values()
        cur_pos = cursor_values.index(self.cursor)
        new_pos = cur_pos + pos

        cursor_options = self.cursor_options()

        cursor_options[self.cursor].unfocus()
        self.cursor = cursor_values[new_pos % len(cursor_values)]
        cursor_options[self.cursor].focus()

    def cursor_input(self, key):
        cursor_options = self.cursor_options()

        if key == 'KEY_UP':
            self.move_cursor(-1)
            return True
        if key == 'KEY_DOWN':
            self.move_cursor(1)
            return True
        if key == 'KEY_LEFT' and self.cursor in ['cancel', 'submit']:
            self.move_cursor(-1)
            return True
        if key == 'KEY_RIGHT' and self.cursor in ['cancel', 'submit']:
            self.move_cursor(1)
            return True

        if self.cursor is not None:
            return cursor_options[self.cursor].input(key)

        return False
