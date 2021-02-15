
class FormObject():

    def init_form_object(self):
        self.display = "visible"
        self.enabled = True
        self.focused = False

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
