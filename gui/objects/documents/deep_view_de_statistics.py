from gui.objects.documents.document import Document, Word, DocumentLine, NewLine, Result, Link, Table
from gui.objects.documents.density_estimation_result import DensityEstimationResultDocument

def report_line(title, result):
    tword = Word(title, {'align': 'left'})
    rword = Result(result, {'align': 'right'})
    return DocumentLine([6, 6], [tword, rword])

class DeepViewDensityEstimatorStatistics(Document):

    def __init__(self, statistics, parameters=None):
        self.statistics = statistics
        title = "Density Estimator statistics"
        metadata = {}
        text_parts = []

        text_parts.append(report_line("Overall score: ", statistics['score']))
        text_parts.append(Word("Estimation score: "))
        text_parts.append(report_line("  Minimum: ", statistics['min_score']))
        text_parts.append(report_line("  Maximum: ", statistics['max_score']))
        text_parts.append(report_line("  Average: ", statistics['avg_score']))
        text_parts.append(report_line("  Standard deviation: ", statistics['std_score']))
        text_parts.append(NewLine())
        text_parts.append(Word("Experiment position: "))
        text_parts.append(report_line("  Minimum: ", statistics['min_pos']))
        text_parts.append(report_line("  Maximum: ", statistics['max_pos']))
        text_parts.append(report_line("  Average: ", statistics['avg_pos']))
        text_parts.append(report_line("  Standard deviation: ", statistics['std_pos']))

        text_parts.append(NewLine())

        text_parts.append(Word("Experiments: ", {'align': 'center'}))

        self.participations = statistics['participations']
        experiments = list(self.participations.keys())

        table = Table([{'size': 2, 'options': {'align': 'left'}}, {'size': 6, 'options': {'align': 'left'}}, {'size': 2, 'options': {'align': 'center'}}, {'size': 2, 'options': {'align': 'right'}}])
        table.add_header(['No.', 'Name', 'Score', 'Pos'])

        if parameters is not None and 'sort_by' in parameters:
            sort_key = parameters['sort_by']
            if sort_key is None:
                sort_key = 'name'

            def sorter(item):
                v = self.participations[sort_key]
                if sort_key == 'score':
                    v = 1/v
                return v

            experiments = sorted(experiments, key=sorter)

        for i in range(len(experiments)):
            name = experiments[i]
            s = self.participations[name]
            table.add_row([Word(str(i+1).rjust(len(str(len(experiments))))), Word(name), Result(s['score']), Result(s['pos'])])

        text_parts += table.get_lines()

        super().__init__(title, metadata, text_parts)
