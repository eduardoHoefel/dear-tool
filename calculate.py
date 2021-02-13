import numpy as np

class Calculate():

    def error(base, e, method='auto'):
        v = [base, e]

        if method == 'auto':
            method = 'perc'

        if method == 'diff':
            return max(v) - min(v)
        if method == 'perc':
            return "{0:.4f} %".format(100 * (1 - (min(v) / max(v))))
        if method == 'log2':
            return int(np.log2(1 - (min(v) / max(v))))

        return Calculate.error(base, e)

    def score(base, e, method='auto'):
        v = [base, e]

        if method == 'auto':
            method = 'log2'

        if method == 'perc':
            return "{0:.4f} %".format(100 * (min(v) / max(v)))

        if method == 'log2':
            if min(v) == max(v):
                return 32

            return -int(np.log2(1 - (min(v) / max(v))))

        return Calculate.score(base, e)
