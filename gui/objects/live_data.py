from gui.objects.renderable import Renderable
from gui.window import Line, LineObject

class LiveData(Renderable):

    def __init__(self, data_provider, formatter):
        super().__init__()
        self.data_provider = data_provider
        self.formatter = formatter

    def render(self, renderer):
        data = self.data_provider()
        formatted = self.formatter(data)
        line = Line()
        lo = LineObject(formatted, 0, {'align': 'right'})
        line.add(lo)
        line.render(renderer)
    
