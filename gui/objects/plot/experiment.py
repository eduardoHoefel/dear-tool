import matplotlib.pyplot as plt
from gui.objects.plot.controller import PlotDataController

class ExperimentPlotDataController(PlotDataController):

    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment

    def get_x_axis_options(self):
        return {'estimator': "Estimator"}

    def get_y_axis_options(self):
        return {'result': "Result", 'score': "Score"}

    def get_lines(self, y, style):
        lines = {}
        estimators = self.experiment.get_estimator_keys()
        estimator_names = [float(x) for x in self.experiment.get_estimator_names()]

        lines_data = []
        auto_estimator_lines = []
        auto_estimator = False
        for key in estimators:
            e = self.experiment.estimators[key]
            data = ''
            if y == 'result':
                data = e.review.estimation
            if y == 'score':
                data = e.review.score

            if "AUTO" in e.name:
                auto_estimator_lines.append(data)
                lines_data.append(0 if style == "bars" else None)
                auto_estimator = True
            else:
                lines_data.append(data)
                auto_estimator_lines.append(0 if style == "bars" else None)

        lines["Estimations"] = (estimator_names, lines_data)
        if auto_estimator:
            lines["Auto parameter"] = (estimator_names, auto_estimator_lines)


        return lines

    def prepare(self, x, y, style):
        for line_label, line in self.get_lines(y, style).items():
            labels, data = line

            self.add_data(labels, data, line_label, style)

        if y == 'result':
            real = [self.experiment.real_value for x in labels]
            self.add_data(labels, real, "Real value", 'real')

    
