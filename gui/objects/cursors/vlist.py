import gui.objects.keys as Keys
from gui.objects.cursors.cursor import Cursor

class VListCursor(Cursor):

    def __init__(self, cursor_items):
        cursor_list = list(cursor_items.keys())
        cursor_map = {}

        for i in range(len(cursor_list)):
            c = cursor_list[i]
            left = None if i == 0 else cursor_list[i-1]
            right = None if i+1 == len(cursor_list) else cursor_list[i+1]
            c_map = {}
            c_map[Keys.UP] = left
            c_map[Keys.DOWN] = right
            cursor_map[c] = c_map

        super().__init__(cursor_map, cursor_items)
