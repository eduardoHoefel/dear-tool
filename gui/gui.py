import curses

READY = 0
RUNNING = 1

from gui.controllers.main import MainMenu
from gui.controllers.quick_actions import QuickActionsMenu
from gui.window import Window, Renderer
from storage import Storage

import time

TASK_FPS = 1
INPUT_FPS = 60

class Gui():

    def __init__(self, stdscr):
        self.height, self.width = stdscr.getmaxyx()
        self.begin_y = 0
        self.begin_x = 0
        self.last_render = None

        self.height -= 1

        self.s = Storage()

        self.win = stdscr

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        stdscr.clear()

        def main_window(title):
            return Window(title, -2, 0, 2, 0, self)

        def quick_actions(title):
            return Window(title, 3, 0, 0, 0, self)

        main = MainMenu(main_window)
        self.quick_actions = QuickActionsMenu(quick_actions, main.window)

        self.windows = [self.quick_actions, main]

        self.running = True
        self.had_task = False
        self.update_fps(INPUT_FPS)

        while self.running:
            self.render()
            self.tick()

    def update_fps(self, fps):
        self.fps = fps
        self.update_frequency = 1/self.fps
        self.force_next_render = True

    def quit(self):
        self.running = False

    def tick(self):
        current_task = self.s.get('task')
        if current_task is not None:
            self.had_task = True
            self.update_fps(TASK_FPS)
            current_task()
            return

        if self.had_task is True:
            self.had_task = False
            self.update_fps(INPUT_FPS)
            return

        c = self.win.getkey()

        r = self.windows[-1].input(c)
        if not r:
            self.windows[0].input(c)

        new_window = self.s.get('new_window')
        if new_window is not None:
            self.windows.append(new_window)
            self.s.set('new_window', None)

        remove_window = self.s.get('remove_window')
        if remove_window is not None:
            self.windows.remove(remove_window)
            self.s.set('remove_window', None)
            if remove_window == self.quick_actions:
                self.running = False

    def render(self):
        cur_time = time.time()
        if not self.force_next_render and (self.last_render is not None and (cur_time - self.last_render) < self.update_frequency):
            return

        self.force_next_render = False
        Renderer.reset_cursor()
        self.win.clear()
        for w in self.windows:
            w.render()
        self.refresh()

        self.last_render = time.time()

    def refresh(self):
        self.win.refresh()
