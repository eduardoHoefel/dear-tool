import time
from gui.objects.progress_bar import ProgressBar
from gui.objects.documents.density_estimation_result import DensityEstimationResultDocument
from gui.objects.documents.experiment_result import ExperimentResultDocument

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
            self.finished = True

    def update_progress(self, progress):
        self.progress = progress

    def get_progress(self):
        return self.progress

    def estimate_time_left(self):
        return self.get_avg_step_time() * (self.get_total_steps() - self.get_steps())

    def get_total_steps(self):
        return self.total_steps

    def get_avg_step_time(self):
        return self.get_steps() / self.get_running_time()

    def get_last_step_time(self):
        return self.last_step_time

    def get_steps(self):
        return self.steps_taken

    def get_running_time(self):
        return time.time() - self.start if not self.finished else self.end - self.start

    def get_document_parameters(self):
        return {}

    def get_document(self, parameters=None):
        pass

class EstimatorExecutor(Executor):

    def __init__(self, estimator):
        super().__init__(1)
        self.estimator = estimator

    def step_exec(self, step):
        self.estimator.run()
        self.update_progress(1)
        return True

    def get_document_parameters(self):
        return {}

    def get_document(self, parameters=None):
        return DensityEstimationResultDocument(self.estimator)

class ExperimentExecutor(Executor):

    def __init__(self, experiment):
        experiment.prepare()
        self.estimator_keys = experiment.get_estimator_keys()
        self.experiment = experiment
        super().__init__(len(self.estimator_keys))

        self.experiment = experiment

    def step_exec(self, step):
        if step < 0 or step >= len(self.estimator_keys):
            #something wrong. lets stop
            return True

        self.experiment.run_estimator(self.estimator_keys[step])
        self.update_progress((step+1)/len(self.estimator_keys))
        return step+1 == len(self.estimator_keys)

    def get_document_parameters(self):
        experiment_parameters = list(self.experiment.parameters.keys())
        default_sort_by = ['name', 'result', 'score']
        return {'sort_by': default_sort_by + experiment_parameters}

    def get_document(self, parameters=None):
        return ExperimentResultDocument(self.experiment, parameters)
