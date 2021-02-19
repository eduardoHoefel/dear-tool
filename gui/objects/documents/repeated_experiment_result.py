from gui.objects.documents.document import Document, Word, DocumentLine, NewLine, Result, Link, Table
from gui.objects.documents.deep_view_de_statistics import DeepViewDensityEstimatorStatistics

def report_line(title, result):
    tword = Word(title, {'align': 'left'})
    rword = Result(result, {'align': 'right'})
    return DocumentLine([6, 6], [tword, rword])

class RepeatedExperimentResultDocument(Document):

    def __init__(self, repeated_experiment, parameters):
        self.repeated_experiment = repeated_experiment
        title = "Repeated Experiment Results"
        metadata = {}
        text_parts = []

        text_parts.append(Word("Estimators: ", {'align': 'center'}))

        self.statistics = repeated_experiment.statistics
        estimations = list(self.statistics.keys())

        table = Table([{'size': 2, 'options': {'align': 'left'}}, {'size': 8, 'options': {'align': 'left'}}, {'size': 2, 'options': {'align': 'center'}}])
        table.add_header(['No.', 'Name', 'Score'])

        if parameters is not None and 'sort_by' in parameters:
            sort_key = parameters['sort_by']
            if sort_key is None:
                sort_key = 'name'

            def sorter(item):
                v = self.statistics[item][sort_key]
                if sort_key == 'score':
                    v = 1/v
                return v

            estimations = sorted(estimations, key=sorter)

        for i in range(len(estimations)):
            name = estimations[i]
            s = self.statistics[name]
            table.add_row([Word(str(i+1).rjust(len(str(len(estimations))))), Link(name, name, self.open), Result(s['score'])])

        text_parts += table.get_lines()

        super().__init__(title, metadata, text_parts)

    def provide_document_from_url(self, url):
        estimator = self.statistics[url]
        def provider(self):
            return DeepViewDensityEstimatorStatistics(estimator)
        return provider

