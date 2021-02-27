import matplotlib.pyplot as plt

class PlotDataController():

    def get_lines(self):
        return []

    def add_data(self, labels, data, label, style):
        if style == "lines":
            self.ax.plot(labels, data, label=label)
        elif style == "dots":
            self.ax.scatter(labels, data, label=label)
        elif style == "bars":
            self.ax.bar(labels, data, label=label)

    def prepare(self, ax):
        pass

    def plot(self, x, y, style):
        fig, ax = plt.subplots()
        self.ax = ax

        self.prepare(x, y, style)

        self.ax = None

        ax.legend()
        plt.show()

    
