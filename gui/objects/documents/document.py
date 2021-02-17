from gui.window import Renderer
import numpy as np
from gui.objects.renderable import Renderable
import gui.objects.keys as Keys
import gui.colors as Colors

class ScrollBar(Renderable):
    def __init__(self, view_size, total_size):
        super().__init__()
        self.update_progress(0)
        self.bar_size = view_size / total_size

    def update_progress(self, progress):
        self.progress = progress

    def render(self, renderer):
        if self.bar_size >= 1:
            return 1

        bar_characters = int(self.bar_size * renderer.height)
        renderer.addstr(0, 0, "╦")
        for i in range(1, renderer.height):
            if i >= round(self.progress * renderer.height) and i <= bar_characters + round(self.progress * renderer.height):
                renderer.addstr(i, 0, "█")
            else:
                renderer.addstr(i, 0, "║")

        renderer.addstr(renderer.height, 0, "╩")
        return 1

class Word(Renderable):
    def __init__(self, text, options=None):
        super().__init__()
        self.text = str(text)
        self.options = options

    def render(self, renderer):
        padding = renderer.width - len(self.text)
        to_render = self.text

        if self.options is not None:
            if 'align' in self.options:
                if self.options['align'] == 'center':
                    to_render = "{}{}".format(" " * int(padding/2), self.text)
                if self.options['align'] == 'right':
                    to_render = "{}{}".format(" " * int(padding), self.text)
        renderer.addstr(0, 0, to_render, self.options)
        return 1

class Result(Word):
    def __init__(self, text, options={}):
        options.update({'bold': True})
        super().__init__("{:8f}".format(float(text)) if type(text) in [float, np.float64] else text, options)

class Title(Word):
    def __init__(self, text):
        super().__init__(text, {'align': 'center', 'color': Colors.TITLE, 'bold': True})

class Link(Word):
    def __init__(self, text, on_click, options={}):
        super().__init__(text, options)
        self.options['bold'] = True
        self.options['color'] = Colors.LINK
        self.on_click = on_click
        self.accessed = False

    def focus(self):
        super().focus()
        self.options['underline'] = True

    def unfocus(self):
        super().focus()
        self.options['underline'] = False

    def input(self, key):
        if key in Keys.ENTER:
            self.on_click()
            self.accessed = True
            self.options['color'] = Colors.ACCESSED_LINK
            return True
        return False

class DocumentLine(Renderable):
    def __init__(self, layout, elements):
        self.elements = elements
        super().__init__()
        self.layout = layout

    def unfocus(self):
        super().unfocus()
        for e in self.elements:
            e.unfocus()

    def focus(self):
        super().focus()
        for e in self.elements:
            e.focus()

    def render(self, renderer):
        acc = 0
        for i in range(len(self.elements)):
            width = int(renderer.width * self.layout[i]/12) if i < len(self.elements)-1 else renderer.width - acc

            sub_renderer = Renderer(0, width, 0, acc, renderer)
            acc += width
            self.elements[i].render(sub_renderer)

        return 1

class NewLine(Renderable):
    def __init__(self):
        super().__init__()
        self.disable()

    def render(self, renderer):
        return 1

class Document():
    def __init__(self, title, metadata, text_parts=[]):
        super().__init__()
        self.title = title
        self.metadata = metadata
        self.text_parts = []
        self.text_parts.append(Title(title))
        self.text_parts.append(NewLine())
        self.text_parts += text_parts

    def get_size(self):
        return len(self.text_parts)

    def get_view(self, start, end):
        return {i: self.text_parts[i] for i in [self.text_parts.index(j) for j in self.text_parts[start:end]]}
