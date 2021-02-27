import matplotlib.pyplot as plt
from gui.objects.plot.controller import PlotDataController

class ExperimentPlotDataController(PlotDataController):

    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment

    def get_x_axis_options(self):
        return {'estimator': "Estimator"}

    def get_y_axis_options(self):
        return {'result': "Result"}

    def get_x_axis_tick_labels(self, x):
        if x == 'estimator':
            return self.experiment.get_estimator_keys()
        return ['']

    def get_lines(self, y):
        lines = {}
        estimators = self.experiment.get_estimator_keys()
        lines_data = []
        auto_estimator_lines = []
        auto_estimator = False
        for name in estimators:
            e = self.experiment.estimators[name]
            data = ''
            if y == 'result':
                data = e.review.estimation

            if "AUTO" in name:
                auto_estimator_lines.append(data)
                lines_data.append(None)
                auto_estimator = True
            else:
                lines_data.append(data)
                auto_estimator_lines.append(None)

        lines["Estimations"] = (estimators, lines_data)
        if auto_estimator:
            lines["Auto parameter"] = (estimators, auto_estimator_lines)


        return lines

    def prepare(self, x, y, style):
        for line_label, line in self.get_lines(y).items():
            labels, data = line

            self.add_data(labels, data, line_label, style)

        if y == 'result':
            real = [self.experiment.real_value for x in labels]
            self.add_data(labels, real, "Real value", 'lines')

    
