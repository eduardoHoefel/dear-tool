
class FormObject():

    def init_form_object(self):
        self.on_change_do = None
        self.default = None
        self.unfocus()
        self.reset()

    def reset(self):
        self.value = self.default
        self.enable()
        self.show()

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def show(self):
        self.display = "visible"

    def hide(self):
        self.display = "hidden"

    def disappear(self):
        self.display = None

    def visible(self):
        return self.display == "visible"

    def hidden(self):
        return self.display == "hidden"

    def is_valid(self):
        return True

    def on_change(self, on_change_func):
        self.on_change_do = on_change_func

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
