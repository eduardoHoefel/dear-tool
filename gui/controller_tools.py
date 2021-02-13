from gui.window import Window, Renderer

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


    def render(self, r1):
        height = len(self.options.keys()) + 2
        r2 = Renderer(height, 0, r1.end_y - r1.begin_y - height + 1, 0, r1)
        #r2.render()
        pos_y = 0
        for key in self.options.keys():
            if key == 'b':
                #quit should be the last option
                continue

            pos_y = self.render_option(key, pos_y, r2)

        pos_y = self.render_option('b', height-3, r2)

        r2.addstr(height-1, 0, "Choose your option: ")

class ParameterChanger():

    def __init__(self, window, name, parameter, back, options=None):
        self.name = name
        self.parameter = parameter
        self.options = options
        self.window = window.popup(5, 40, 'center')
        self.back = back

    def render(self):
        self.window.render()
        pass

    def input(self, key):
        return False

class ParameterController():

    def __init__(self):
        self.parameters = {}

    def can_run(self):
        for p in self.parameters.values():
            if p['required'] and (not p['value'] or not p['default']):
                return False
        return True

    def add_parameter(self, key, name, default, required):
        self.parameters[key] = {'name': name, 'default': default, 'required': required, 'value': None}

    def render_parameter(self, key, pos_y, renderer):
        p = self.parameters[key]
        if p['required'] and (not p['value'] and not p['default']):
            checked_str = " "
        else:
            checked_str = "X"

        name = p['name']
        name_tabs = "\t" * int((20 - len(name))/8)

        value_str = p['value']

        default_str = "default = {}".format(p['default']) if p['default'] else "no default value"
        required_str = "Required" if p['required'] else "Optional"

        renderer.addstr(pos_y, 0, "[{}] {}: {}{}\t({})\t{}".format(checked_str, name, name_tabs, value_str, default_str, required_str))
        pos_y += 1

        return pos_y

    def render(self, r1):
        height = len(self.parameters.keys())
        r2 = Renderer(-3, 0, 3, 0, r1)
        pos_y = 0
        for key in self.parameters.keys():
            pos_y = self.render_parameter(key, pos_y, r2)
