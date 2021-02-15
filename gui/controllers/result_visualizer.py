from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.controllers.task_controller import TaskController
from gui.window import Renderer
from gui.objects.document import DocumentViewer

class ResultVisualizer(WindowController):

    def __init__(self, window_provider, executable):
        title = "Results"
        super().__init__(title, window_provider)

        self.results = executable.get_output()
        self.document = DocumentViewer(self.results)

        def back_window_provider(title):
            return self.window.internal_renderer.popup(3, 4+len(title), 'bottom', title)

        self.back = Button("Back", back_window_provider, self.on_back)

    def on_back(self):
        self.remove()
        pass

    def input(self, key):
        return self.back.input(key)

    def render(self):
        super().render()
        renderer = Renderer(0, -4, 0, 4, self.window.internal_renderer)
        self.document.render(renderer)
        self.back.render()
        pass
