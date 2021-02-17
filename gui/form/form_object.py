from gui.objects.renderable import Renderable

class FormObject(Renderable):

    def init_form_object(self, default=None):
        self.default = default
        super().__init__()
        self.on_change_do = None
        self.reset()

    def reset(self):
        super().reset()
        self.set_value(self.default)

    def set_value(self, value):
        pass

    def on_change(self, on_change_func):
        self.on_change_do = on_change_func

    def get_value(self):
        return None

    def input(self, key):
        old_value = self.get_value()
        r = self.handle_input(key)
        new_value = self.get_value()

        if old_value != new_value:

            self.changed(old_value, new_value)

        return r

    def changed(self, old_value=str, new_value=str):
        if old_value == str:
            old_value = self.get_value()
        if new_value == str:
            new_value = self.get_value()

        if self.on_change_do is not None:
            self.on_change_do(old_value, new_value, self.is_valid())
