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
        self.win.addstr(pos_y+self.begin_y, pos_x+self.begin_x, text)

    def clear(self):
        for i in range(self.height):
            self.addstr(i, 0, " " * self.width)

    def render(self):
        rectangle(self.win, self.begin_y, self.begin_x, self.end_y, self.end_x)
        #self.win.addstr(self.end_y, self.begin_x, "{} [{}, {}, {}, {}]({}x{})".format(self.name, self.begin_y, self.end_y, self.begin_x, self.end_x, self.height, self.width))

class Window(Renderer):
    def __init__(self, height, width, begin_y, begin_x, parent):
        super().__init__(height, width, begin_y, begin_x, parent)
        self.name = "Window"

        self.internal_renderer = Renderer(-2, -2, 1, 1, self)

    def render(self):
        super().render()
        self.internal_renderer.clear()

    def popup(self, height, width, pos='center'):
        if pos == 'center':
            pos_y = int((self.height - height)/2)
            pos_x = int((self.width - width)/2)

        if pos == 'bottom':
            pos_y = -height - 1 if height < 0 else self.height - height - 1
            pos_x = 1

        return Window(height, width, pos_y, pos_x, self)

