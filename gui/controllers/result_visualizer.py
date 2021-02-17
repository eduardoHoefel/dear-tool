from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.controllers.task_controller import TaskController
from gui.window import Window, Renderer
from gui.objects.documents.viewer import DocumentViewer
from gui.objects.cursors.hcycle import HCycleCursor

class ResultVisualizer(WindowController):

    def __init__(self, window_provider, executable):
        super().__init__(None, window_provider)

        def viewer_window_provider(title):
            return Window(None, -3, -1, 3, 0, self.window.internal_renderer)

        self.results = executable.get_output()
        self.document = DocumentViewer(viewer_window_provider, self.results)

        def back_window_provider(title):
            return self.window.internal_renderer.popup(3, 4+len("Back"), 'top', title)

        self.back = Button("Back", back_window_provider, self.on_back)
        self.cursor = HCycleCursor({'document': self.document, 'back': self.back})

    def on_back(self):
        self.remove()

    def input(self, key):
        return self.cursor.input(key)

    def render(self):
        super().render()

        def renderer_provider(index, pos_y, cursor, item):
            if pos_y is None:
                pos_y = 0
            return pos_y, None

        self.cursor.render(renderer_provider)
