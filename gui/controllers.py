from gui.window import Window, Renderer
from gui.controller_tools import Menu, ParameterController, ParameterChanger

from estimators.known_formula import KnownFormula
from estimators.real import Real

class WindowController():

    def __init__(self, window, back):
        self.window = window
        self.back = back

    def render(self):
        pass

    def input(self, key):
        return False

class QuickActionsMenu(WindowController):

    def __init__(self, window, quit):
        super().__init__(window, quit)
        self.popup = None

    def input(self, key):
        if self.popup is not None:
            return self.popup.input(key)

        if key == 'q':
            self.back()
            return True

    def render(self):
        self.window.render()
        r1 = self.window.internal_renderer
        r1.addstr(0, 0, "[q] Quit  [i] Import datafile [c] Create syntetic datafile")
        r1.addstr(1, -1, "├")
        r1.addstr(1, r1.width, "┤")

        if self.popup is not None:
            self.popup.render()

    def recover(self):
        self.popup = None

class MainMenu(WindowController):

    def __init__(self, window, back):
        super().__init__(window, back)
        self.menu = Menu()
        self.menu.add_option('d', 'Density estimator', self.estimator)
        self.menu.add_option('e', 'Experiment', self.experiment)
        self.menu.add_option('s', 'Statistal analysis of experiments', self.experiment_statistics)

        self.popup = None

    def input(self, key):
        if self.popup is not None:
            return self.popup.input(key)

        return self.menu.input(key)

    def render(self):
        self.window.render()
        self.menu.render(self.window.internal_renderer)

        if self.popup is not None:
            self.popup.render()

    def recover(self):
        self.popup = None

    def estimator(self):
        self.popup = EstimatorController(self.window.popup(-5, -2, 'bottom'), self.recover)
        pass

    def experiment(self):
        self.change_controller(None)
        pass

    def experiment_statistics(self):
        self.change_controller(None)
        pass

class EstimatorController(WindowController):

    def __init__(self, window, back):
        super().__init__(window, back)

        self.parameter_controller = ParameterController()
        self.parameter_controller.add_parameter('data', 'Data', None, True)
        self.parameter_controller.add_parameter('estimator', 'Estimator', None, True)

        self.parameter_changer = None

        self.menu = Menu(self.back)
        self.menu.add_option('d', 'Change datafile', self.set_datafile)
        self.menu.add_option('e', 'Change estimator', self.set_estimator)
        self.menu.add_option('m', 'Change mean', self.set_mean, self.needs_mean)
        self.menu.add_option('s', 'Change standard deviation', self.set_std, self.needs_std)
        self.menu.add_option('r', 'Run', self.run_experiment, self.parameter_controller.can_run)

    def run_experiment(self):
        pass

    def recover(self):
        self.parameter_changer = None

    def input(self, key):
        if self.parameter_changer is not None:
            self.parameter_changer.input(key)
            return True

        return self.menu.input(key)

    def render(self):
        self.window.render()
        self.parameter_controller.render(self.window.internal_renderer)
        self.menu.render(self.window.internal_renderer)

        if self.parameter_changer is not None:
            self.parameter_changer.render()

    def set_estimator(self):
        pass

    def set_datafile(self):
        #self.parameter_controller.parameters['data']['value'] = 2
        self.parameter_changer = ParameterChanger(self.window, 'Datafile', self.parameter_controller.parameters['data'], self.recover)

    def set_synthetic_data(self):
        self.parameter_changer = ParameterChanger(self.window, 'Synthetic data', self.parameter_controller.parameters['data'])

    def set_mean(self):
        pass

    def set_std(self):
        pass

    def needs_mean(self):
        return self.parameter_controller.parameters['estimator'] in [KnownFormula, Real]

    def needs_std(self):
        return self.parameter_controller.parameters['estimator'] in [KnownFormula, Real]
