import matplotlib.pyplot as plt

class PlotDataController():

    def get_lines(self):
        return []

    def add_data(self, labels, data, label, style):
        if style == "lines":
            self.ax.plot(labels, data, label=label)
        elif style == "real":
            self.ax.plot(labels, data, 'k-', label=label)
        elif style == "dots":
            self.ax.scatter(labels, data, label=label)
        elif style == "bars":
            self.ax.bar(labels, data, label=label)

    def prepare(self, ax):
        pass


    def adjust(self, fig, ax):
        adjust={}
        adjust['left'] = .08
        adjust['bottom'] = .1
        adjust['right'] = .996
        adjust['top'] = .988
        adjust['wspace'] = 0.16
        adjust['hspace'] = .178
    
        fig.tight_layout()
    
        plt.subplots_adjust(**adjust)

    def plot(self, x, y, style):
        fig, ax = plt.subplots()
        self.ax = ax

        self.prepare(x, y, style)

        if x == 'estimator':
            self.ax.set_xlabel('Estimator parameter')
        if x == 'samples':
            self.ax.set_ylabel('Samples')

        if y == 'result':
            self.ax.set_ylabel('Calculated entropy')
        if y == 'score':
            self.ax.set_ylabel('Score')

        ax.legend()
        self.adjust(fig, ax)

        plt.show()

        self.ax = None

    
