
class Renderable():

    def __init__(self):
        self.reset()

    def reset(self):
        self.unfocus()
        self.enable()
        self.show()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False

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

    def input(self, key):
        return False

    def render(self, renderer=None):
        return 0
