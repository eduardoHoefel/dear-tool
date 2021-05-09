import matplotlib.pyplot as plt
from gui.objects.plot.controller import PlotDataController

class RepeatedExperimentPlotDataController(PlotDataController):

    def __init__(self, repeated_experiment):
        super().__init__()
        self.repeated_experiment = repeated_experiment

    def get_x_axis_options(self):
        return {'estimator': "Estimator", 'samples': "Samples"}

    def get_y_axis_options(self):
        return {'result': "Result", 'score': "Score"}

    def get_lines(self, x, y):
        if x == 'estimator':
            estimators = self.repeated_experiment.get_estimator_keys()
            estimator_names = self.repeated_experiment.get_experiment_example().get_estimator_names()
            line_data = []
            for key in estimators:
                e = self.repeated_experiment.statistics[key]
                data = ''
                if y == 'result':
                    data = e['avg_result']
                if y == 'score':
                    data = e['avg_score']

                line_data.append(data)


            return {"Estimations": (estimator_names, line_data)}

        if x == 'samples':
            samples = self.repeated_experiment.get_samples()
            estimators = self.repeated_experiment.get_estimator_keys()
            estimator_names = self.repeated_experiment.get_experiment_example().get_estimator_names()
            lines = {}
            for i, key in enumerate(estimators):
                name = estimator_names[i]
                if y == 'result':
                    line_data = list(self.repeated_experiment.results[key].values())
                if y == 'score':
                    line_data = list(self.repeated_experiment.scores[key].values())
                lines[name] = (samples, line_data)

            return lines

    def prepare(self, x, y, style):
        for line_name, line_data in self.get_lines(x, y).items():
            labels, data = line_data

            self.add_data(labels, data, line_name, style)

        if y == 'result':
            real = [e.real_value for e in self.repeated_experiment.experiments.values()]
            self.add_data(labels, real, "Real value", 'lines')

    
