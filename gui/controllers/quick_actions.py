from gui.controllers.window_controller import WindowController
from gui.controllers.create_syntetic_datafile import CreateSynteticDatafileController

class QuickActionsMenu(WindowController):

    def __init__(self, window_provider, main_window):
        title = "[q] Quit  [i] Import datafile [c] Create syntetic datafile"
        super().__init__(title, window_provider)
        self.main_window = main_window

    def input(self, key):
        if key == 'q':
            self.remove()
            return True

        if key == 'i':
            return True

        if key == 'c':
            def window_provider(title):
                return self.main_window.popup(10, 45, 'center', title)

            popup = CreateSynteticDatafileController(window_provider)
            WindowController.add(popup)



    def render(self):
        super().render()
        #r1 = self.window.internal_renderer
        #r1.addstr(0, 0, "[q] Quit  [i] Import datafile [c] Create syntetic datafile")
