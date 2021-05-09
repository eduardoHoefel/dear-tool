from gui.objects.documents.document import Document, Word, DocumentLine, NewLine, Result, Link, Table
from gui.objects.documents.density_estimation_result import DensityEstimationResultDocument

def report_line(title, result):
    tword = Word(title, {'align': 'left'})
    rword = Result(result, {'align': 'right'})
    return DocumentLine([6, 6], [tword, rword])

class ExperimentResultDocument(Document):

    def __init__(self, experiment, parameters):
        self.experiment = experiment
        title = "Experiment Results"
        metadata = {}
        text_parts = []

        datafile = experiment.estimators[list(experiment.estimators.keys())[0]].datafile
        if datafile.density is not None:
            text_parts.append(report_line("Known density: ", datafile.density))

        text_parts.append(NewLine())
        text_parts.append(Word("Estimations: ", {'align': 'center'}))

        estimations = list(experiment.estimators.values())
        table = Table([{'size': 2, 'options': {'align': 'left'}}, {'size': 5, 'options': {'align': 'left'}}, {'size': 3, 'options': {'align': 'right'}}, {'size': 2, 'options': {'align': 'center'}}])
        table.add_header(['No.', 'Name', 'Result', 'Score'])

        if parameters is not None and 'sort_by' in parameters:
            sort_key = parameters['sort_by']

            def sorter(item):
                v = item.get_sort_value(sort_key)
                return v

            estimations = sorted(estimations, key=sorter)

        for i in range(len(estimations)):
            e = estimations[i]
            table.add_row([Word(str(i+1).rjust(len(str(len(estimations))))), Link(e.name, e.id, self.open), Result(e.output), Word(e.review.score)])

        text_parts += table.get_lines()

        super().__init__(title, metadata, text_parts)

    def provide_document_from_url(self, url):
        estimator = self.experiment.estimators[url]
        def provider(self):
            return DensityEstimationResultDocument(estimator)
        return provider

