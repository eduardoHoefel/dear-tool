from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.controllers.task_controller import TaskController
from gui.window import Window, Renderer
from gui.objects.documents.viewer import DocumentViewer
from gui.objects.cursors.cycle import CycleCursor
from gui.objects.cursors.hlist import HListCursor
from gui.objects.cursors.vlist import VListCursor
from gui.objects.cursors.list import ListCursor
from gui.objects.cursors.cursor import Cursor
import estimators.all as Estimators
from gui.form.section import Section
from gui.form.select import Select
from gui.window import Renderer

class DocumentWindow(WindowController):

    def __init__(self, window_provider, document_provider, window_options={}):
        super().__init__(None, window_provider)
        self.window_options = window_options
        self.document_provider = document_provider


        def back_window_provider(title):
            return self.window.internal_renderer.popup(3, 4+len("Back"), 'top', title)

        self.back = Button("Back", back_window_provider, self.on_back)


        def viewer_window_provider(title):
            return Window(None, -3, -1, 3, 0, self.window.internal_renderer)

        self.document_viewer = DocumentViewer(viewer_window_provider)
        self.prepare_document()

        if 'sort_by' in window_options.keys():
            sort_option_keys = window_options['sort_by']
            sort_option_names = Estimators.get_all_input_names()
            sort_options = {k: sort_option_names[k] for k in sort_option_keys}
            select = Select(False, sort_options, 0)
            section = Section("Sort by: ", select)
            def on_select_change(old_value, new_value, is_valid):
                parameters = {} if not is_valid else {'sort_by': new_value}
                self.prepare_document(parameters)

            select.on_change(on_select_change)
            select.changed()

            self.cursor = VListCursor({'buttons': HListCursor({'back': self.back, 'sort': section}) , 'document_viewer': self.document_viewer})
            self.cursor.current().go_to('sort')

        else:
            self.cursor = CycleCursor({'document_viewer': self.document_viewer, 'back': self.back})

    def prepare_document(self, parameters=None):
        document = self.document_provider(parameters)
        self.get_document_provider_from_url = document.get_document_provider()
        document.set_url_opener(self.on_link_click)
        self.document_viewer.set_document(document)

    def on_link_click(self, url):
        if self.get_document_provider_from_url is None:
            return

        document_provider = self.get_document_provider_from_url(url)
        self.open(document_provider)

    def open(self, document_provider):
        def get_window(title):
            return self.window.parent.parent.popup(0, 0, 'center', title)

        popup = DocumentWindow(get_window, document_provider)
        WindowController.add(popup)

    def on_back(self):
        self.remove()

    def input(self, key):
        return self.cursor.input(key)

    def render(self):
        super().render()

        def renderer_provider(index, pos_y, cursor, item):
            padding = 10
            if pos_y is None:
                pos_y = 0
            return pos_y, Renderer(1, -padding-2, 1, padding, self.window.internal_renderer)

        def cursor_renderer_provider(index, pos_y, cursor, item):
            if issubclass(type(item), Cursor):
                return 0, renderer_provider

            return 0, renderer_provider(index, pos_y, cursor, item)

        self.cursor.render(cursor_renderer_provider)
