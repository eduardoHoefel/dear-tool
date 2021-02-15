import time
from gui.objects.progress_bar import ProgressBar
from gui.objects.document import DensityEstimationResultDocument

class Executor():

    def __init__(self):
        self.started = False
        self.finished = False
        self.steps_taken = 0
        self.last_step_time = None
        self.progress = 0
        self.output = None

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
        return Document(self.output)

class EstimatorExecutor(Executor):

    def __init__(self, estimator):
        super().__init__()
        self.estimator = estimator

    def step_exec(self, step):
        self.output = self.estimator.estimate()
        self.update_progress(1)
        return True

    def get_output(self):
        return DensityEstimationResultDocument(self.estimator, self.output)
