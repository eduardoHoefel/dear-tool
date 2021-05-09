
class Datafile():

    def __init__(self, data, pdf, pdf_params):
        self.data = data
        self.samples = len(data)
        self.pdf = pdf
        self.pdf_params = pdf_params
        self.density = None

    def get_data(self):
        return self.data

    def set_density(self, density):
        self.density = density

    def split(self, samples):
        data2 = self.data[:samples]
        datafile = Datafile(data2, self.pdf, self.pdf_params)
        datafile.set_density(self.density)
        return datafile

