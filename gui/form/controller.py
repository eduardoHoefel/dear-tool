from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.window import Renderer
from gui.objects.cursor_manager import CursorManager
import gui.colors as Colors

class FormController(WindowController, CursorManager):

    def __init__(self, window_provider):
        super().__init__(None, window_provider)
        self.elements = {}
        self.cursor = None

    def add_button(self, key, title, on_press):
        def window_provider(faketitle):
            return self.window.popup(3, 4+len(title), 'bottom' if key == 'cancel' else 'bottom-right', None)
        self.elements[key] = Button(title, window_provider, on_press, Colors.SUCCESS if key == 'submit' else Colors.DEFAULT)

    def start(self):
        self.input(None)
        cursor_options = self.interactible_cursor_options()
        self.cursor = list(cursor_options.keys())[0]
        cursor_options[self.cursor].focus()


    def get_data(self):
        data = {}
        for key in self.elements.keys():
            data[key] = self.elements[key].get_value()

        return data

    def can_submit(self):
        editable = self.interactible_cursor_options()
        for p in self.elements.keys():
            if p in editable and not self.elements[p].is_valid():
                return False
        return True

    def add_input(self, key, inp):
        self.elements[key] = inp

    def interactible_cursor_options(self):
        cursor_options = self.renderable_cursor_options()
        interactible_keys = [k for k in cursor_options.keys() if cursor_options[k].is_enabled() and cursor_options[k].visible()]
        options = {}
        for key in interactible_keys:
            options[key] = cursor_options[key]

        return options

    def cursor_values(self):
        cursor_values = list(self.elements.keys())
        cursor_values = [c for c in cursor_values if self.elements[c].visible()]

        return cursor_values

    def renderable_cursor_options(self):
        return self.elements

        #options = {}
        #keys = self.cursor_values()
        #for key in keys:
        #    options[key] = self.elements[key]

        #return options

    def input(self, key):
        r = self.cursor_input(key)

        if 'submit' in self.elements:
            submit = self.elements['submit']
            if self.can_submit():
                submit.enable()
                if r is False and key in ['KEY_ENTER', '\n']:
                    r = submit.input(key)
            else:
                submit.disable()

        return r

    def render(self):
        renderer = self.window

        tbr = self.renderable_cursor_options()

        tbr_original = self.cursor_values()
        tbr_order = self.cursor_values()

        drawn_at_pos = {}

        pos_x = 0

        for obj in tbr_order:
            drawn_at_pos[obj] = pos_x
            renderer = Renderer(1, -1, pos_x, 0, self.window)
            pos_x += tbr[obj].render(renderer)

        renderer = Renderer(1, -1, drawn_at_pos[self.cursor], 0, self.window)
        tbr[self.cursor].render(renderer)

