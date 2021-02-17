from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.window import Renderer
from gui.objects.cursors.vcycle import VCycleCursor
import gui.colors as Colors
import gui.objects.keys as Keys

class FormController(WindowController):

    def __init__(self, window_provider):
        super().__init__(None, window_provider)
        self.elements = {}
        self.action_buttons = {}
        self.cursor = None
        self.submit = None

    def set_action_button(self, action, button):
        self.action_buttons[action] = button

    def get_button(self, key, title, on_press):
        def window_provider(faketitle):
            return self.window.popup(3, 4+len(title), 'bottom' if key == 'cancel' else 'bottom-right', None)
        return Button(title, window_provider, on_press, Colors.SUCCESS if key == 'submit' else Colors.DEFAULT)

    def start(self):
        self.cursor = VCycleCursor(self.elements)
        self.cursor.set_filter(self.cursor_filter)
        self.cursor.set_draw_filter(self.draw_filter)
        self.input(None)

    def get_data(self):
        data = {}
        for key in self.elements.keys():
            data[key] = self.elements[key].get_value()

        return data

    def cursor_filter(self, key, el):
        return el.is_enabled() and el.visible()

    def can_submit(self):
        editable = {k: v for k, v in self.elements.items() if self.cursor_filter(k, v)}
        for k, v in editable.items():
            if not v.is_valid():
                return False

        return True

    def add_element(self, key, inp):
        self.elements[key] = inp

    def draw_filter(self, key, el):
        return el.visible()

    def input(self, key):
        r = self.cursor.input(key)

        if 'submit' in self.action_buttons.keys():
            submit = self.action_buttons['submit']
            if self.can_submit():
                submit.enable()
                if r is False and key in Keys.ENTER:
                    return submit.input(key)
            else:
                submit.disable()

        if 'cancel' in self.action_buttons.keys():
            pass

        return r

    def render(self):
        def renderer_provider(index, pos_y, cursor, item):
            if pos_y is None:
                pos_y = 0

            return pos_y, Renderer(1, -1, pos_y, 0, self.window)

        self.cursor.render(renderer_provider)

