from gui.controllers.window_controller import WindowController
from gui.form.form_object import FormObject

class Button(WindowController, FormObject):

    def __init__(self, name, window_provider, action):
        super().__init__(name, window_provider)
        self.init_form_object()
        self.name = name
        self.action = action
        self.focused = False

    def input(self, key):
        import log
        log.debug(key)
        if key in ['KEY_ENTER', '\n', '\r']:
            self.action()
            return True
        return False

    def render(self, renderer=None):
        if self.visible():
            super().render()
        #r1 = self.window.internal_renderer
        #r1.addstr(0, 0, self.name)



