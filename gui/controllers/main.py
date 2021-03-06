from gui.tools import Menu
from gui.controllers.window_controller import WindowController
from gui.controllers.estimator import EstimatorController
from gui.controllers.experiment import ExperimentController
from gui.controllers.repeated_experiment_analysis import RepeatedExperimentAnalysisController
from gui.controllers.pde_contest import PDEContestController
from gui.static.textfile_reader import TextfileReader
import gui.colors as Colors

class MainMenu(WindowController):

    def __init__(self, window_provider):
        title = TextfileReader.read("resources/title.txt")

        super().__init__(title, window_provider, window_render_options={'merge_top_borders': True, 'color': Colors.BIG_TITLE})
        self.menu = Menu()
        self.menu.add_option('d', 'Density estimation', self.estimator)
        self.menu.add_option('e', 'Experiment', self.experiment)
        self.menu.add_option('r', 'Repeated experiment analysis', self.repeated_experiment_analysis)
        self.menu.add_option('p', 'PDE contest', self.pde_contest)

        self.s.set('datafiles', [])
        self.s.set('executions', [])


    def input(self, key):
        return self.menu.input(key)

    def render(self):
        super().render()
        renderer = self.window.internal_renderer

        datafiles = self.s.get('datafiles')
        max_datafiles = 5

        if len(datafiles) == 0:
            renderer.addstr(0, 1, "Import or create a datafile to start")
        else:
            renderer.addstr(0, 1, "Imported datafiles: {}".format(len(datafiles)))
            for i in range(max_datafiles):
                if i in datafiles:
                    d = datafiles[i]
                    renderer.addstr(2 + i, 5, d)

#        executions = self.s.get('executions')
#        max_executions = 5
#
#        if len(executions) == 0:
#            renderer.addstr(8, 1, "No executions so far")
#        else:
#            renderer.addstr(8, 1, "Executions: {}".format(len(executions)))
#            for i in range(max_executions):
#                if i in executions:
#                    d = executions[i]
#                    renderer.addstr(10 + i, 5, d)

        self.menu.render(self.window.internal_renderer)

    def estimator(self):
        def get_window(title):
            return self.window.internal_renderer.popup(-1, -2, 'bottom', title)

        popup = EstimatorController(get_window)
        WindowController.add(popup)

    def experiment(self):
        def get_window(title):
            return self.window.internal_renderer.popup(-1, -2, 'bottom', title)

        popup = ExperimentController(get_window)
        WindowController.add(popup)

    def repeated_experiment_analysis(self):
        def get_window(title):
            return self.window.internal_renderer.popup(-1, -2, 'bottom', title)

        popup = RepeatedExperimentAnalysisController(get_window)
        WindowController.add(popup)

    def pde_contest(self):
        def get_window(title):
            return self.window.internal_renderer.popup(-1, -2, 'bottom', title)

        popup = PDEContestController(get_window)
        WindowController.add(popup)
