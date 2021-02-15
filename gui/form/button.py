from gui.controllers.window_controller import WindowController
from gui.form.form_object import FormObject
import gui.colors as Colors

class Button(WindowController, FormObject):

    def __init__(self, name, window_provider, action, default_color=Colors.DEFAULT):
        super().__init__(None, window_provider)
        self.init_form_object()
        self.name = name
        self.action = action
        self.focused = False
        self.default_color = default_color

    def input(self, key):
        if key in ['KEY_ENTER', '\n', '\r']:
            self.action()
            return True
        return False

    def render(self, renderer=None):
        if self.visible():
            super().render()
        r1 = self.window.internal_renderer
        color = Colors.ERROR if self.enabled is False else self.default_color
        options = {'color': color}
        r1.addstr(0, 1, self.name, options)



