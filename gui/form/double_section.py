from gui.form.form_object import FormObject
from gui.window import Line, LineObject
import gui.colors as Colors
from gui.window import Renderer
from gui.objects.cursors.hcycle import HCycleCursor
import gui.objects.keys as Keys

class DoubleSection(FormObject):

    def __init__(self, section1, section2):
        self.sections = {0: section1, 1: section2}
        self.cursor = HCycleCursor(self.sections)
        self.init_form_object(section1.default)
        self.cursor.set_filter(self.cursor_filter)

    def cursor_filter(self, key):
        el = self.sections[key]
        return el.is_enabled() and el.visible()

    def set_value(self, value):
        pass

    def unfocus(self):
        super().unfocus()
        self.sections[0].unfocus()
        self.sections[1].unfocus()

    def focus(self):
        super().focus()
        if not self.cursor.current().is_enabled():
            self.cursor.move(Keys.RIGHT)


    def enable(self):
        super().enable()
        self.sections[0].enable()
        self.sections[1].enable()

    def disable(self):
        super().disable()
        self.sections[0].disable()
        self.sections[1].disable()

    def show(self):
        super().show()
        self.sections[0].show()
        self.sections[1].show()

    def hide(self):
        super().hide()
        self.sections[0].hide()
        self.sections[1].hide()
    
    def disappear(self):
        super().disappear()
        self.sections[0].disappear()
        self.sections[1].disappear()

    def is_valid(self):
        return self.sections[0].is_valid() and self.sections[1].is_valid()

    def on_change(self, on_change_func):
        pass

    def get_value(self):
        return [s.get_value() for k, s in self.sections.items()]

    def input(self, key):
        r = self.cursor.input(key)
        return r

    def render(self, renderer):
        separator = "  "
        width = renderer.width - len(separator)

        half_width =  int(width/2-1.5)
        half_width2 = int(width/2-1)
        sizes = [half_width, half_width2]
        positions = [0, half_width + len(separator)]

        def renderer_provider(index, pos_y, cursor, item):
            return sizes[index], Renderer(1, sizes[index], positions[index], 0, renderer)

        self.cursor.render(renderer_provider)

        return 1
