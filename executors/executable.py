import time
from gui.objects.progress_bar import ProgressBar
from gui.objects.documents.density_estimation_result import DensityEstimationResultDocument

class Executor():

    def __init__(self, total_steps):
        self.started = False
        self.finished = False
        self.steps_taken = 0
        self.last_step_time = None
        self.progress = 0
        self.total_steps = total_steps

    def start(self):
        if self.started:
            return

        self.started = True
        self.start = time.time()

    def step(self):
        if self.finished:
            return

        step_start = time.time()
        is_over = self.step_exec(self.steps_taken)
        step_end = time.time()
        self.last_step_time = step_end - step_start
        self.steps_taken += 1

        if is_over:
            self.end = time.time()
            self.compute_statistics()
            self.finished = True

    def update_progress(self, progress):
        self.progress = progress

    def get_progress(self):
        return self.progress

    def compute_statistics(self):
        self.total_time = self.end - self.start

    def render(self, renderer):
        width = renderer.width - 1
        progress = self.get_progress()

        perc = int(progress * 100)
        perc_str = (str(perc).rjust(3) + " %")
        perc_str = perc_str.rjust(int((2+width+len(perc_str))/2))
        progress_bar = ProgressBar.progress_bar_str(progress, width)

        renderer.addstr(0, 0, progress_bar)
        renderer.addstr(1, 0, perc_str)
        pass

    def get_output(self):
        pass

class EstimatorExecutor(Executor):

    def __init__(self, estimator):
        super().__init__(1)
        self.estimator = estimator

    def step_exec(self, step):
        self.estimator.run()
        self.update_progress(1)
        return True

    def get_output(self):
        return DensityEstimationResultDocument(self.estimator)

class ExperimentExecutor(Executor):

    def __init__(self, experiment):
        self.estimator_keys = experiment.get_estimator_keys()
        super().__init__(len(self.estimator_keys))

        self.experiment = experiment
        experiment.prepare()

    def step_exec(self, step):
        if step < 0 or step >= len(self.estimator_keys):
            #something wrong. lets stop
            return True

        self.experiment.run_estimator(self.estimator_keys[step])
        self.update_progress((step+1)/len(self.estimator_keys))
        return step+1 == len(self.estimator_keys)

    def get_output(self):
        return DensityEstimationResultDocument(self.experiment.estimators[self.estimator_keys[0]])
