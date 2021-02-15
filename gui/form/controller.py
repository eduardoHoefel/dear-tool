from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.window import Renderer
from gui.objects.cursor_manager import CursorManager
import gui.colors as Colors

class FormController(WindowController, CursorManager):

    def __init__(self, window_provider, on_cancel, on_submit):
        super().__init__(None, window_provider)
        self.inputs = {}
        self.on_submit = on_submit
        self.cursor = 'cancel'

        def cancel_window_provider(title):
            return self.window.popup(3, 4+len("Cancel"), 'bottom', title)


        def submit_window_provider(title):
            return self.window.popup(3, 4+len("Button"), 'bottom-right', title)


        self.cancel = Button("Cancel", cancel_window_provider, on_cancel)

        self.submit = Button("Submit", submit_window_provider, self.submit, Colors.SUCCESS)

    def start(self):
        self.input(None)

    def submit(self):
        data = self.get_data()
        self.on_submit(data)

    def get_data(self):
        data = {}
        for key in self.inputs.keys():
            data[key] = self.inputs[key].get_value()

        return data

    def can_submit(self):
        editable = self.interactible_cursor_options()
        for p in self.inputs.keys():
            if p in editable and not self.inputs[p].is_valid():
                return False
        return True

    def add_input(self, key, inp):
        self.inputs[key] = inp

        if self.cursor == 'cancel':
            self.move_cursor(-1)

    def interactible_cursor_options(self):
        cursor_options = self.renderable_cursor_options()
        interactible_keys = [k for k in cursor_options.keys() if cursor_options[k].enabled]
        options = {}
        for key in interactible_keys:
            options[key] = cursor_options[key]

        return options


    def cursor_values(self):
        cursor_values = list(self.inputs.keys())
        cursor_values = [c for c in cursor_values if self.inputs[c].visible()]
        cursor_values.append('cancel')
        cursor_values.append('submit')
        return cursor_values

    def renderable_cursor_options(self):
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
        r = self.cursor_input(key)

        if not r:
            if key in ['KEY_ENTER', '\n']:
                if self.can_submit():
                    r = self.submit.input(key)

        if self.can_submit():
            self.submit.enable()
        else:
            self.submit.disable()

        return r

    def render(self):
        renderer = self.window

        tbr = self.renderable_cursor_options()

        tbr_original = self.cursor_values()
        tbr_order = self.cursor_values()

        tbr_order.remove(self.cursor)
        tbr_order.append(self.cursor)


        for obj in tbr_order:
            renderer = Renderer(1, 0, tbr_original.index(obj), 0, self.window)
            tbr[obj].render(renderer)
