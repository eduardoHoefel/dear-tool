import curses
from curses.textpad import Textbox, rectangle

class Renderer():

    def __init__(self, height, width, begin_y, begin_x, parent):
        self.height = height if height > 0 else parent.height + height
        self.width = width if width > 0 else parent.width + width
        self.begin_y = begin_y + parent.begin_y
        self.begin_x = begin_x + parent.begin_x

        self.end_y = self.begin_y + self.height - 1
        self.end_x = self.begin_x + self.width - 1

        self.parent = parent
        self.win = parent.win
        self.name = "Renderer"

    def addstr(self, pos_y, pos_x, text):
        self.win.addstr(pos_y+self.begin_y, pos_x+self.begin_x, str(text))

    def clear(self):
        for i in range(self.height):
            self.addstr(i, 0, " " * self.width)

    def render(self, options=None):
        rectangle(self.win, self.begin_y, self.begin_x, self.end_y, self.end_x)

        if options is not None:
            for k in options:
                if k == 'merge_top_borders':
                    self.addstr(0, 0, "├")
                    self.addstr(0, self.width-1, "┤")
        #self.win.addstr(self.end_y, self.begin_x, "{} [{}, {}, {}, {}]({}x{})".format(self.name, self.begin_y, self.end_y, self.begin_x, self.end_x, self.height, self.width))

    def popup(self, height, width, pos, title):
        if pos == 'center':
            pos_y = -int(height/2) if height <= 0 else int((self.height - height)/2)
            pos_x = -int(width/2) if width <= 0 else int((self.width - width)/2)

        if pos == 'bottom':
            pos_y = -height - 1 if height <= 0 else self.height - height
            pos_x = 1

        if pos == 'bottom-right':
            pos_y = -height - 1 if height <= 0 else self.height - height
            pos_x = self.width - width - 1

        return Window(title, height, width, pos_y, pos_x, self)

class Window(Renderer):
    def __init__(self, title, height, width, begin_y, begin_x, parent):
        super().__init__(height, width, begin_y, begin_x, parent)
        self.title = title

        title_lines = len(title)+1 if type(title) == list else 0 if title == None else 2

        self.name = "Window"

        self.internal_renderer = Renderer(-(2 + title_lines), -2, title_lines + 1, 1, self)

    def render(self, options=None):
        self.clear()
        super().render(options)
        if self.title is not None:
            if type(self.title) == str:
                self.addstr(1, 2, self.title)
            if type(self.title) == list:
                for i in range(len(self.title)):
                    line = self.title[i]
                    self.addstr(i+1, 2, line)


