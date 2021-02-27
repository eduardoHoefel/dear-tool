
class Datafile():

    def __init__(self, data, m=None, s=None, f=None):
        self.data = data
        self.samples = len(data)
        self.m = m
        self.s = s
        self.f = f
        self.density = None

    def get_data(self):
        return self.data

    def set_density(self, density):
        self.density = density

    def split(self, samples):
        data2 = self.data[:samples]
        datafile = Datafile(data2, self.m, self.s, self.f)
        datafile.set_density(self.density)
        return datafile

