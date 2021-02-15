from estimators.analysis import EstimationAnalysis
import numpy as np

class TextAdjuster():
    def __init__(self, width):
        self.width = width

    def adjust(self, left_part, right_part):
        text = left_part + right_part.rjust(self.width - len(left_part))
        return text

class Document():
    def __init__(self, text=None):
        self.text_parts = []
        if text is not None:
            self.append("", text)

    def append(self, left_part, right_part=""):
        if type(right_part) in [float, np.float64]:
            right_part = "{:.8f}".format(right_part)

        self.text_parts.append((str(left_part), str(right_part)))

    def print(self, adjuster):
        b = ""
        for part in self.text_parts:
            b += adjuster.adjust(part[0], part[1]) + "\n"

        return b


class DensityEstimationResultDocument(Document):
    def __init__(self, estimator, result):
        super().__init__()

        datafile = estimator.datafile
        if datafile.m is not None:
            self.append("Known mean: ", datafile.m)
        if datafile.s is not None:
            self.append("Known std deviation: ", datafile.s)
        if datafile.density is not None:
            self.append("Known density: ", datafile.density)

        self.append("\n")
        self.append("Density Estimation: ", result)
        if datafile.density is not None:
            review = EstimationAnalysis(result, datafile.density)
            self.append("Error (raw): ", review.raw)
            self.append("Error (relative): ", review.relative)
            self.append("Score: ", review.score)

class DocumentViewer():

    def __init__(self, text_provider):
        self.text_provider = text_provider
        self.cur_line = 0
        self.last_print = None
        self.adjuster = None

    def render(self, renderer):
        if self.adjuster is None:
            self.adjuster = TextAdjuster(renderer.width)

        if self.last_print is None:
            self.last_print = self.text_provider.print(self.adjuster)

        text = self.last_print

        text_lines = text.split("\n")

        lines_that_fit = min(len(text_lines), renderer.height)

        for i in range(lines_that_fit):
            line = text_lines[i+self.cur_line]
            renderer.addstr(i, 0, line)




