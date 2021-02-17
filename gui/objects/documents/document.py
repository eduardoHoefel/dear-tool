from gui.window import Renderer
import numpy as np
from gui.objects.renderable import Renderable
import gui.objects.keys as Keys
import gui.colors as Colors
from gui.objects.cursors.hlist import HListCursor

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

        bar_characters = max(1, round(self.bar_size * renderer.height))
        renderer.addstr(0, 0, "╦")
        for i in range(1, renderer.height):
            if i >= round(self.progress * renderer.height) and i <= bar_characters + round(self.progress * renderer.height):
                renderer.addstr(i, 0, "█")
            else:
                renderer.addstr(i, 0, "║")

        renderer.addstr(renderer.height, 0, "╩")
        return 1

class Word(Renderable):
    def __init__(self, text, options={}):
        self.options = options
        super().__init__()
        self.text = str(text)

    def render(self, renderer):
        padding = renderer.width - len(self.text)
        to_render = self.text

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
    def __init__(self, text, url, on_click, options={}):
        super().__init__(text, options)
        self.options['bold'] = True
        #self.options['color'] = Colors.LINK
        self.on_click = on_click
        self.url = url
        self.accessed = False

    def input(self, key):
        if key in Keys.ENTER:
            self.on_click(self.url)
            self.accessed = True
            return True
        return False

    def render(self, renderer):
        self.options['color'] = Colors.ACCESSED_LINK if self.accessed else Colors.LINK
        self.options['underline'] = self.focused
        r = super().render(renderer)
        del self.options['color']
        del self.options['underline']
        return r

class DocumentLine(Renderable):
    def __init__(self, layout, elements):
        self.cursor = HListCursor({k: elements[k] for k in range(len(elements))})
        super().__init__()
        self.layout = layout
        self.basic_margin = 2

    def unfocus(self):
        super().unfocus()
        self.cursor.unfocus()

    def focus(self):
        super().focus()
        self.cursor.focus()

    def input(self, key):
        self.cursor.input(key)

    def get_padding(self, i, renderer_width):
        acc = 0
        for j in range(i):
            acc += self.get_width(j, renderer_width)
            acc += self.basic_margin

        return acc

    def get_width(self, i, renderer_width):
        width = int(renderer_width * self.layout[i]/12) if i < len(self.layout)-1 else renderer_width - self.get_padding(i, renderer_width)
        return width

    def render(self, renderer):
        acc = 0

        def renderer_provider(index, pos_y, cursor, item):
            width = self.get_width(index, renderer.width)
            padding = self.get_padding(index, renderer.width)
            return 0, Renderer(0, width, 0, padding, renderer)

        self.cursor.render(renderer_provider)

        return 1

class Table():

    def __init__(self, layout):
        self.layout = [{'size': v['size'], 'options': {} if 'options' not in v else v['options']} for v in layout]
        self.lines = []

    def get_line_layout(self):
        return [x['size'] for x in self.layout]

    def add_row(self, columns):
        words = []
        for i in range(len(columns)):
            obj = columns[i]
            options = self.layout[i]['options']
            if obj.options is not None:
                obj.options.update(options)
            else:
                obj.options = {k: v for k, v in options.items()}

            words.append(obj)

        self.lines.append(DocumentLine(self.get_line_layout(), words))

    def add_header(self, columns):
        words = []
        for i in range(len(columns)):
            options = {k: v for k, v in self.layout[i]['options'].items()}
            options['bold'] = True
            #options['align'] = 'center'
            words.append(Word(columns[i], options))

        self.lines.append(DocumentLine(self.get_line_layout(), words))

    def get_lines(self):
        return self.lines


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
        self.set_url_opener(None)

    def provide_document_from_url(self, url):
        return None

    def get_document_provider(self):
        return self.provide_document_from_url

    def set_url_opener(self, url_opener):
        self.url_opener = url_opener

    def open(self, url):
        if self.url_opener is not None:
            self.url_opener(url)

    def get_size(self):
        return len(self.text_parts)

    def get_view(self, start, end):
        return {i: self.text_parts[i] for i in [self.text_parts.index(j) for j in self.text_parts[start:end]]}
