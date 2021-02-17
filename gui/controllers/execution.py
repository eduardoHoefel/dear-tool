from gui.form.button import Button
from gui.controllers.window_controller import WindowController
from gui.controllers.task_controller import TaskController
from gui.objects.cursors.cycle import CycleCursor
from gui.objects.progress_bar import ProgressBar
from gui.objects.live_data import LiveData
from gui.form.section import Section
from gui.static.formatter import Formatter

from gui.controllers.result_visualizer import DocumentWindow

from gui.window import Renderer

class ExecutionController(WindowController):

    def __init__(self, window_provider, executable):
        title = None
        super().__init__(title, window_provider, {'align': 'center'})
        self.executable = executable

        def back_window_provider(title):
            return self.window.internal_renderer.popup(3, 4+len("Back"), 'bottom', title)

        def visualize_window_provider(title):
            return self.window.internal_renderer.popup(3, 4+len("Visualize"), 'bottom-right', title)

        self.back = Button("Back", back_window_provider, self.on_back)

        self.visualize = Button("Visualize", visualize_window_provider, self.on_visualize)

        progress_bar = ProgressBar(executable.get_progress)

        live_time_progress = LiveData(executable.get_running_time, Formatter.timedelta_to_string)        
        live_time_expected = LiveData(executable.estimate_time_left, Formatter.timedelta_to_string)        

        time_progress_section = Section("Running time", live_time_progress)
        expected_time_section = Section("Time to finish", live_time_expected)
        self.cursor = CycleCursor({'0': progress_bar, '1': time_progress_section, '2': expected_time_section, 'visualize': self.visualize, 'back': self.back})

        def cursor_filter(key, elem):
            return key in ['back', 'visualize']

        self.cursor.set_filter(cursor_filter)

        executable.start()
        TaskController.set(self.run)

    def run(self):
        self.executable.step()

        if self.executable.finished is True:
            TaskController.remove()

    def input(self, key):
        return self.cursor.input(key)

    def on_back(self):
        self.remove()
        pass

    def on_visualize(self):
        self.remove()
        def get_window(title):
            return self.window.parent.parent.popup(-5, -5, 'center', title)

        popup = DocumentWindow(get_window, self.executable.get_document, self.executable.get_document_parameters())
        WindowController.add(popup)

    def render(self):
        self.window.title = "Complete" if self.executable.finished else "Executing"
        super().render()

        if self.executable.finished is True:
            self.back.show()
            self.visualize.show()
        else:
            self.back.hide()
            self.visualize.hide()

        def renderer_provider(index, pos_y, cursor, item):
            if pos_y is None:
                pos_y = 2

            return pos_y, Renderer(0, -3, pos_y, 1, self.window.internal_renderer)

        self.cursor.render(renderer_provider)


