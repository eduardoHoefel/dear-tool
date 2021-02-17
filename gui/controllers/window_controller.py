from storage import Storage

class WindowController():

    def add(window):
        Storage().set('new_window', window)

    def __init__(self, title, window_provider, window_render_options=None):
        self.window = window_provider(title)
        self.window_render_options = window_render_options
        self.s = Storage()

    def set_active(self, active):
        self.window.active = active

    def render(self, more_options={}):
        options = {}
        options.update(more_options)
        if self.window_render_options is not None:
            options.update(self.window_render_options)

        self.window.render(options)
        pass

    def input(self, key):
        return False

    def remove(self):
        self.s.set('remove_window', self)
