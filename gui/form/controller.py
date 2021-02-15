from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.window import Renderer
from gui.objects.cursor_manager import CursorManager

class FormController(WindowController, CursorManager):

    def __init__(self, window_provider, on_cancel, on_submit):
        super().__init__(None, window_provider)
        self.inputs = {}
        self.on_submit = on_submit
        self.cursor = 'cancel'

        def cancel_window_provider(title):
            return self.window.popup(3, 4+len(title), 'bottom', title)


        def submit_window_provider(title):
            return self.window.popup(3, 4+len(title), 'bottom-right', title)


        self.cancel = Button("Cancel", cancel_window_provider, on_cancel)

        self.submit = Button("Submit", submit_window_provider, self.submit)

    def submit(self):
        data = self.get_data()
        self.on_submit(data)

    def get_data(self):
        data = {}
        for key in self.inputs.keys():
            data[key] = self.inputs[key].get_value()

        return data

    def can_submit(self):
        for p in self.inputs.values():
            if not p.is_valid():
                return False
        return True

    def add_input(self, key, inp):
        self.inputs[key] = inp

        if self.cursor == 'cancel':
            self.move_cursor(-1)

    def cursor_values(self):
        cursor_values = list(self.inputs.keys())
        cursor_values = [c for c in cursor_values if self.inputs[c].visible()]
        cursor_values.append('cancel')
        cursor_values.append('submit')
        return cursor_values

    def cursor_options(self):
        options = {}
        keys = self.cursor_values()
        for key in keys:
            if key in self.inputs:
                options[key] = self.inputs[key]
            if key == 'cancel':
                options[key] = self.cancel
            if key == 'submit':
                options[key] = self.submit

        return options

    def input(self, key):
        return self.cursor_input(key)

    def render(self):
        renderer = self.window

        tbr = self.cursor_options()

        tbr_original = self.cursor_values()
        tbr_order = self.cursor_values()

        tbr_order.remove(self.cursor)
        tbr_order.append(self.cursor)


        for obj in tbr_order:
            renderer = Renderer(1, 0, tbr_original.index(obj), 0, self.window)
            tbr[obj].render(renderer)
