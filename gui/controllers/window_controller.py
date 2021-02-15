from storage import Storage

class WindowController():

    def add(window):
        Storage().set('new_window', window)

    def __init__(self, title, window_provider, window_render_options=None):
        self.window = window_provider(title)
        self.window_render_options = window_render_options
        self.s = Storage()

    def render(self):
        self.window.render(self.window_render_options)
        pass

    def input(self, key):
        return False

    def remove(self):
        self.s.set('remove_window', self)
