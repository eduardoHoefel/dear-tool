import curses

READY = 0
RUNNING = 1

from gui.controllers import MainMenu
from gui.controllers import QuickActionsMenu
from gui.window import Window

class Gui():

    def __init__(self, stdscr):
        self.height, self.width = stdscr.getmaxyx()
        self.begin_y = 0
        self.begin_x = 0

        self.height -= 1

        self.win = stdscr
        curses.use_default_colors()
        stdscr.clear()

        main_window = Window(-2, 0, 2, 0, self)
        quick_actions_window = Window(3, 0, 0, 0, self)

        self.main = MainMenu(main_window, None)
        self.quick_actions = QuickActionsMenu(quick_actions_window, self.quit)
        self.running = True

        while self.running:
            self.render()
            self.tick()

    def quit(self):
        self.running = False

    def tick(self):
        c = self.win.getkey()
        r = self.main.input(c)
        if not r:
            self.quick_actions.input(c)

    def render(self):
        self.win.clear()
        self.main.render()
        self.quick_actions.render()
        self.refresh()

    def addstr(self, pos_y, pos_x, text):
        self.win.addstr(pos_y, pos_x, text)

    def refresh(self):
        self.win.refresh()
