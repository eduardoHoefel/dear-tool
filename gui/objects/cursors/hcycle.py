import gui.objects.keys as Keys
from gui.objects.cursors.cursor import Cursor

class HCycleCursor(Cursor):

    def __init__(self, cursor_items):
        cursor_map = {}
        cursor_list = list(cursor_items.keys())

        for i in range(len(cursor_list)):
            c = cursor_list[i]
            left = cursor_list[(len(cursor_list)+i-1) % len(cursor_list)]
            right = cursor_list[(i+1) % len(cursor_list)]
            c_map = {}
            c_map[Keys.LEFT] = left
            c_map[Keys.RIGHT] = right
            cursor_map[c] = c_map

        super().__init__(cursor_map, cursor_items)
