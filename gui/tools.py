from gui.window import Renderer

class Menu():

    def __init__(self, back=None):
        self.options = {}
        self.names = {}
        self.available_checks = {}

        if back is not None:
            self.add_option('b', 'Back', back)

    def add_option(self, key, name, f, available_check=None):
        self.options[key] = f
        self.names[key] = name
        if available_check is not None:
            self.available_checks[key] = available_check

    def input(self, key):
        if key in self.options:
            self.options[key]()
            return True

        return False

    def render_option(self, key, pos_y, renderer):
        if key not in self.options.keys():
            return pos_y

        if key in self.available_checks.keys():
            check = self.available_checks[key]
            if not check():
                return pos_y

        renderer.addstr(pos_y, 0, "[{}]: {}".format(key, self.names[key]))
        pos_y += 1

        return pos_y


    def render(self, renderer):
        height = len(self.options.keys()) + 2
        r2 = Renderer(height, 0, renderer.end_y - renderer.begin_y - height + 1, 0, renderer)
        #r2.render()
        pos_y = 0
        for key in self.options.keys():
            if key == 'b':
                #quit should be the last option
                continue

            pos_y = self.render_option(key, pos_y, r2)

        pos_y = self.render_option('b', height-3, r2)

        r2.addstr(height-1, 0, "Choose your option: ")

