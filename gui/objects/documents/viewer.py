from gui.controllers.window_controller import WindowController
from estimators.analysis import EstimationAnalysis
from gui.objects.cursors.vlist import VListCursor
from gui.window import Renderer
from gui.form.form_object import FormObject
from gui.objects.documents.document import ScrollBar
import gui.objects.keys as Keys

class DocumentViewer(WindowController, FormObject):

    def __init__(self, window_provider):
        super().__init__(None, window_provider)
        self.init_form_object()


    def set_document(self, document):
        self.document = document
        self.cursor = None
        self.view_start = 0
        self.scroll_bar = ScrollBar(self.window.internal_renderer.height, document.get_size())
        self.update_view()


    def get_view(self, scroll_off=0):
        height = self.window.internal_renderer.height
        view_end = self.view_start + height - 3
        if self.cursor is not None:
            if self.cursor.pos - self.view_start < scroll_off:
                self.view_start -= scroll_off - (self.cursor.pos - self.view_start)
            elif view_end - self.cursor.pos < scroll_off and self.document.get_size() - view_end > scroll_off:
                self.view_start += scroll_off - (view_end - self.cursor.pos)
        self.view_start = max(0, self.view_start)

        view_end = self.view_start + height
        self.scroll_bar.update_progress((self.view_start)/(self.document.get_size()))

        view = self.document.get_view(self.view_start, view_end)
        return view

    def input(self, key):
        r = self.cursor.input(key)

        if key == Keys.ESC and r:
            self.set_document(self.document)
            return True

        self.update_view()

        return r


    def update_view(self):
        height = self.window.internal_renderer.height
        scroll_off = int(height/6)

        old_pos = None if self.cursor is None else self.cursor.pos
        cursor_view = self.get_view(scroll_off)

        self.cursor = VListCursor(cursor_view)
        self.cursor.set_filter(self.cursor_filter)

        if old_pos is not None:
            self.cursor.go_to(old_pos)

    def cursor_filter(self, key, el):
        return el.is_enabled() and el.visible()

    def render(self, renderer=None):
        super().render()

        scrollbar_renderer = Renderer(-1, 1, 0, self.window.width, self.window)
        self.scroll_bar.render(scrollbar_renderer)

        def renderer_provider(index, pos_y, cursor, item):
            if pos_y is None:
                pos_y = 0

            return pos_y, Renderer(1, -2, pos_y, 1, self.window.internal_renderer)

        self.cursor.render(renderer_provider)

        return 0




