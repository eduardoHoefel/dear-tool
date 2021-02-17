
class Cursor():

    def __init__(self, cursor_map, cursor_items):
        self.cursor_map = cursor_map
        self.filter = None
        self.draw_filter = None
        self.cursor_items = cursor_items
        self.pos = None
        self.go_to_first()

    def go_to_first(self):
        cursor_list = list(self.cursor_map.keys())
        for i in range(len(cursor_list)):
            new_pos = cursor_list[i]
            if new_pos == self.pos:
                return
            if self.filter is None or self.filter(new_pos, self.cursor_items[new_pos]) is True:
                self.go_to(new_pos)
                return True

    def go_to_last(self):
        cursor_list = list(self.cursor_map.keys())
        for i in range(len(cursor_list)-1, -1, -1):
            new_pos = cursor_list[i]
            if new_pos == self.pos:
                return
            if self.filter is None or self.filter(new_pos, self.cursor_items[new_pos]) is True:
                self.go_to(new_pos)
                return True

    def go_to(self, pos):
        if self.pos is not None:
            self.cursor_items[self.pos].unfocus()
        self.pos = pos
        self.cursor_items[self.pos].focus()

    def go_to_index(self, index):
        self.go_to(list(self.cursor_map.keys())[index])

    def set_filter(self, f):
        self.filter = f

    def set_draw_filter(self, f):
        self.draw_filter = f

    def current(self):
        return self.cursor_items[self.pos]

    def move(self, key):
        original_pos = self.pos
        new_pos = self.pos
        while True:
            possible_moves = self.cursor_map[new_pos]
            if key not in possible_moves:
                return False

            new_pos = possible_moves[key]
            if new_pos in [None, original_pos]:
                return False

            if self.filter is None or self.filter(new_pos, self.cursor_items[new_pos]) is True:
                self.go_to(new_pos)
                return True


    def input(self, key):
        if key is None:
            return False

        if self.current().input(key):
            return True

        return self.move(key)

    def render(self, renderer_provider):
        tbr_order = {k: v for k, v in self.cursor_items.items() if self.draw_filter is None or self.draw_filter(k, v)}

        renderers_used = {}
        index = 0
        pos_y = None

        for k, v in tbr_order.items():
            pos_y, renderer = renderer_provider(index, pos_y, k, v)
            renderers_used[k] = renderer
            new_pos_y = v.render(renderer)
            pos_y += new_pos_y
            index += 1

        self.current().render(renderers_used[self.pos])
