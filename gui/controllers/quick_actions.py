from gui.controllers.window_controller import WindowController
from gui.controllers.create_synthetic_datafile import CreateSyntheticDatafileController
from gui.controllers.rng_seed import RNGSeedController
import gui.objects.keys as Keys

class QuickActionsMenu(WindowController):

    def __init__(self, window_provider, main_window):
        title = "[q] Quit [s] Set rng seed [c] Create datafile"
        super().__init__(title, window_provider)
        self.main_window = main_window

    def input(self, key):
        if key == 'q' or key == Keys.ESC:
            self.remove()
            return True

        if key == 'i':
            return True

        if key == 's':
            def window_provider(title):
                return self.main_window.popup(11, 45, 'center', title)

            popup = RNGSeedController(window_provider)
            WindowController.add(popup)

            return True

        if key == 'c':
            def window_provider(title):
                return self.main_window.popup(16, 65, 'center', title)

            popup = CreateSyntheticDatafileController(window_provider)
            WindowController.add(popup)

            return True

        return False



    def render(self):
        super().render()
        #r1 = self.window.internal_renderer
        #r1.addstr(0, 0, "[q] Quit  [i] Import datafile [c] Create synthetic datafile")
