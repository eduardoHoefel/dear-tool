from gui.objects.documents.document import Document, Word, DocumentLine, NewLine, Result
from estimators.analysis import EstimationAnalysis

def report_line(title, result):
    tword = Word(title, {'align': 'left'})
    rword = Result(result, {'align': 'right'})
    return DocumentLine([6, 6], [tword, rword])

class DensityEstimationResultDocument(Document):

    def __init__(self, estimator):
        title = "Density Estimation Results"
        metadata = {}
        text_parts = []

        datafile = estimator.datafile
        if datafile.m is not None:
            text_parts.append(report_line("Known mean: ", datafile.m))
        if datafile.s is not None:
            text_parts.append(report_line("Known std deviation: ", datafile.s))
        if datafile.density is not None:
            text_parts.append(report_line("Known density: ", datafile.density))

        text_parts.append(NewLine())
        text_parts.append(report_line("Density Estimator: ", estimator.name))
        text_parts.append(report_line("Shannon entropy: ", estimator.output))
        if datafile.density is not None:
            estimator.analyse(datafile.density)
            review = estimator.review
            text_parts.append(report_line("Error (raw): ", review.raw))
            text_parts.append(report_line("Error (relative): ", review.relative))
            text_parts.append(report_line("Score: ", review.score))

        super().__init__(title, metadata, text_parts)
