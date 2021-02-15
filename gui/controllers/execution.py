from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.controllers.task_controller import TaskController
from gui.objects.cursor_manager import CursorManager

from gui.controllers.result_visualizer import ResultVisualizer

from gui.window import Renderer

class ExecutionController(WindowController, CursorManager):

    def __init__(self, window_provider, executable):
        title = None
        super().__init__(title, window_provider)

        self.executable = executable

        def back_window_provider(title):
            return self.window.internal_renderer.popup(3, 4+len(title), 'bottom', title)

        def visualize_window_provider(title):
            return self.window.internal_renderer.popup(3, 4+len(title), 'bottom-right', title)

        self.back = Button("Back", back_window_provider, self.on_back)

        self.visualize = Button("Visualize", visualize_window_provider, self.on_visualize)

        self.cursor = 'submit'

        executable.start()
        TaskController.set(self.run)

    def run(self):
        self.executable.step()

        if self.executable.finished is True:
            TaskController.remove()

    def cursor_values(self):
        return ['cancel', 'submit']

    def cursor_options(self):
        return {'cancel': self.back, 'submit': self.visualize}

    def input(self, key):
        return self.cursor_input(key)

    def on_back(self):
        self.remove()
        pass

    def on_visualize(self):
        self.remove()
        def get_window(title):
            return self.window.parent.parent.popup(-5, -5, 'center', title)

        popup = ResultVisualizer(get_window, self.executable)
        WindowController.add(popup)

    def render(self):
        super().render()

        title = "Complete" if self.executable.finished else "Executing"

        renderer = self.window.internal_renderer
        title = title.rjust(int((renderer.width+len(title))/2))
        renderer.addstr(0, 0, title)

        renderer = Renderer(2, -3, 2, 1, renderer)

        self.executable.render(renderer)

        if self.executable.finished is True:
            self.back.render()
            self.visualize.render()

        pass


