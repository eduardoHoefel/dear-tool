from gui.form.form_object import FormObject
from gui.window import Line, LineObject
import gui.colors as Colors

class SectionBreak(FormObject):

    def __init__(self):
        self.init_form_object(None)
        self.enabled = False

    def handle_input(self, key):
        return False

    def render(self, renderer):
        return 1
