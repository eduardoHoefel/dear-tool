import scipy as sc

class DataProvider():

    def syntetic(m, s, samples):
        return sc.stats.norm.rvs(m, s, samples)
