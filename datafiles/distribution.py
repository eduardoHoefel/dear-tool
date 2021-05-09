all_distributions = []
param_map = {}


def get_parameters(dist):
    stats = dist.stats


    if stats == sc.alpha:
        return ['shape']

class Distribution():

    def __init__(self, stats, name):
        self.stats = stats
        self.name = name
        self.pdf = stats.pdf

        all_distributions.append(self)

    def rvs(self, dist_params, loc, scale, size):
        return self.stats.rvs(*dist_params, loc, scale, size=size)

    def __str__(self):
        return self.name

import scipy.stats as sc

norm = Distribution(sc.norm, "Normal")
alpha = Distribution(sc.alpha, "Alpha")
anglit = Distribution(sc.anglit, "Anglit")
arcsine = Distribution(sc.arcsine, "Arcsine")
argus = Distribution(sc.argus, "Argus")
beta = Distribution(sc.beta, "Beta")
betaprime = Distribution(sc.betaprime, "Beta prime")
bradford = Distribution(sc.bradford, "Bradford")
burr = Distribution(sc.burr, "Burr (Type III)")
burr12 = Distribution(sc.burr12, "Burr (Type XII)")
cauchy = Distribution(sc.cauchy, "Cauchy")
chi = Distribution(sc.chi, "Chi")
chi2 = Distribution(sc.chi2, "Chi-squared")
cosine = Distribution(sc.cosine, "Cosine")
crystalball = Distribution(sc.crystalball, "Crystallball")
dgamma = Distribution(sc.dgamma, "Double gamma")
dweibull = Distribution(sc.dweibull, "Double Weibull")
erlang = Distribution(sc.erlang, "Erlang")
expon = Distribution(sc.expon, "Exponential")
exponnorm = Distribution(sc.exponnorm, "Exponentially modified Normal")
exponweib = Distribution(sc.exponweib, "Exponentiated Weibull")
exponpow = Distribution(sc.exponpow, "Exponential power")
f = Distribution(sc.f, "F")
fatiguelife = Distribution(sc.fatiguelife, "Fatigue-life (Birnbaum-Saunders)")
fisk = Distribution(sc.fisk, "Fisk")
foldcauchy = Distribution(sc.foldcauchy, "Folded Cauchy")
foldnorm = Distribution(sc.foldnorm, "Folded normal")
genlogistic = Distribution(sc.genlogistic, "Generalized logistic")
gennorm = Distribution(sc.gennorm, "Generalized normal")
genpareto = Distribution(sc.genpareto, "Generalized Pareto")
genexpon = Distribution(sc.genexpon, "Generalized exponential")
genextreme = Distribution(sc.genextreme, "Generalized extreme value")
gausshyper = Distribution(sc.gausshyper, "Gauss hypergeometric")
gamma = Distribution(sc.gamma, "Gamma")
gengamma = Distribution(sc.gengamma, "Generalized gamma")
genhalflogistic = Distribution(sc.genhalflogistic, "Generalized half-logistic")
geninvgauss = Distribution(sc.geninvgauss, "Generalized Inverse Gaussian")
gilbrat = Distribution(sc.gilbrat, "Gilbrat")
gompertz = Distribution(sc.gompertz, "Gompertz (or truncated Gumbel)")
gumbel_r = Distribution(sc.gumbel_r, "Right-skewed Gumbel")
gumbel_l = Distribution(sc.gumbel_l, "Left-skewed Gumbel")
halfcauchy = Distribution(sc.halfcauchy, "Half-Cauchy")
halflogistic = Distribution(sc.halflogistic, "Half-logistic")
halfnorm = Distribution(sc.halfnorm, "Half-normal")
halfgennorm = Distribution(sc.halfgennorm, "Upper half of a generalized normal")
hypsecant = Distribution(sc.hypsecant, "Hyperbolic secant")
invgamma = Distribution(sc.invgamma, "Inverted gamma")
invgauss = Distribution(sc.invgauss, "Inverse Gaussian")
invweibull = Distribution(sc.invweibull, "Inverted Weibull")
johnsonsb = Distribution(sc.johnsonsb, "Johnson SB")
johnsonsu = Distribution(sc.johnsonsu, "Johnson SU")
kappa3 = Distribution(sc.kappa3, "Kappa 3")
kappa4 = Distribution(sc.kappa4, "Kappa 4")
ksone = Distribution(sc.ksone, "Kolmogorov-Smirnov one-sided")
kstwo = Distribution(sc.ksone, "Kolmogorov-Smirnov two-sided")
kstwobign = Distribution(sc.ksone, "Scaled Kolmogorov-Smirnov two-sided")
laplace = Distribution(sc.laplace, "Laplace")
laplace_asymmetric = Distribution(sc.laplace_asymmetric, "Asymmetric Laplace")
levy = Distribution(sc.levy, "Levy")
levy_l = Distribution(sc.levy_l, "Left-skewed Levy")
levy_stable = Distribution(sc.levy_stable, "Levy-stable")
logistic = Distribution(sc.logistic, "Logistic (or Sech-squared)")
loggamma = Distribution(sc.loggamma, "Log gamma")
loglaplace = Distribution(sc.loglaplace, "Log-Laplace")
lognorm = Distribution(sc.lognorm, "Lognormal")
loguniform = Distribution(sc.loguniform, "Loguniform or reciprocal")
lomax = Distribution(sc.lomax, "Lomax (Pareto of the second kind)")
maxwell = Distribution(sc.maxwell, "Maxwell")
mielke = Distribution(sc.mielke, "Mielke Beta-Kappa / Dagum")
moyal = Distribution(sc.moyal, "Moyal")
nakagami = Distribution(sc.nakagami, "Nakagami")
ncx2 = Distribution(sc.ncx2, "Non-central chi-squared")
ncf = Distribution(sc.ncf, "Non-central F distribution")
nct = Distribution(sc.nct, "Non-central Student’s t")
norminvgauss = Distribution(sc.norminvgauss, "Normal Inverse Gaussian")
pareto = Distribution(sc.pareto, "Pareto")
pearson3 = Distribution(sc.pearson3, "Pearson type III")
powerlaw = Distribution(sc.powerlaw, "Power function")
powerlognorm = Distribution(sc.powerlognorm, "Power log-normal")
powernorm = Distribution(sc.powernorm, "Power normal")
rdist = Distribution(sc.rdist, "R-distributed (symmetric beta)")
rayleigh = Distribution(sc.rayleigh, "Rayleigh")
rice = Distribution(sc.rice, "Rice")
recipinvgauss = Distribution(sc.recipinvgauss, "Reciprocal inverse Gaussian")
semicircular = Distribution(sc.semicircular, "Semicircular")
skewnorm = Distribution(sc.skewnorm, "Skew-normal")
t = Distribution(sc.t, "Student's t")
trapezoid = Distribution(sc.trapezoid, "Trapezoidal")
triang = Distribution(sc.triang, "Triangular")
truncexpon = Distribution(sc.truncexpon, "Truncated exponential")
truncnorm = Distribution(sc.truncnorm, "Truncated normal")
tukeylambda = Distribution(sc.tukeylambda, "Tukey-Lamdba")
uniform = Distribution(sc.uniform, "Uniform")
vonmises = Distribution(sc.vonmises, "Von Mises")
wald = Distribution(sc.wald, "Wald")
weibull_min = Distribution(sc.weibull_min, "Weibull minimum")
weibull_max = Distribution(sc.weibull_min, "Weibull maximum")
wrapcauchy = Distribution(sc.wrapcauchy, "Wrapped Cauchy")

param_map[alpha] = ['a']
param_map[anglit] = []
param_map[arcsine] = []
param_map[argus] = ['a']
param_map[beta] = ['a', 'b']
param_map[betaprime] = ['a', 'b']
param_map[bradford] = ['a']
param_map[burr] = ['c', 'd']
param_map[burr12] = ['c', 'd']
param_map[cauchy] = []
param_map[chi] = ['a']
param_map[chi2] = ['a']
param_map[cosine] = []
param_map[crystalball] = ['beta', 'm']
param_map[dgamma] = ['a']
param_map[dweibull] = ['a']
param_map[erlang] = ['a']
param_map[expon] = []
param_map[exponnorm] = ['k']
param_map[exponweib] = ['a', 'c']
param_map[exponpow] = ['b']
param_map[f] = ['dfn', 'dfd']
param_map[fatiguelife] = ['c']
param_map[fisk] = ['c']
param_map[foldcauchy] = ['c']
param_map[foldnorm] = ['c']
param_map[genlogistic] = ['c']
param_map[gennorm] = ['beta']
param_map[genpareto] = ['c']
param_map[genexpon] = ['a', 'b', 'c']
param_map[genextreme] = ['c']
param_map[gausshyper] = ['a', 'b', 'c', 'z']
param_map[gamma] = ['a']
param_map[gengamma] = ['a', 'c']
param_map[genhalflogistic] = ['c']
param_map[geninvgauss] = ['p', 'b']
param_map[gilbrat] = []
param_map[gompertz] = ['c']
param_map[gumbel_r] = []
param_map[gumbel_l] = []
param_map[halfcauchy] = []
param_map[halflogistic] = []
param_map[halfnorm] = []
param_map[halfgennorm] = ['beta']
param_map[hypsecant] = []
param_map[invgamma] = ['a']
param_map[invgauss] = ['mu']
param_map[invweibull] = ['c']
param_map[johnsonsb] = ['a', 'b']
param_map[johnsonsu] = ['a', 'b']
param_map[kappa4] = ['h', 'k']
param_map[kappa3] = ['a']
param_map[ksone] = ['n']
param_map[kstwo] = ['n']
param_map[kstwobign] = []
param_map[laplace] = []
param_map[laplace_asymmetric] = ['k']
param_map[levy] = []
param_map[levy_l] = []
param_map[levy_stable] = ['alpha', 'beta']
param_map[logistic] = []
param_map[loggamma] = ['c']
param_map[loglaplace] = ['c']
param_map[lognorm] = ['s']
param_map[loguniform] = ['a', 'b']
param_map[lomax] = ['c']
param_map[maxwell] = []
param_map[mielke] = ['k' 's']
param_map[moyal] = []
param_map[nakagami] = ['v']
param_map[ncx2] = ['df', 'nc']
param_map[ncf] = ['df1', 'df2', 'nc']
param_map[nct] = ['df,' 'nc']
param_map[norm] = []
param_map[norminvgauss] = ['a', 'b']
param_map[pareto] = ['b']
param_map[pearson3] = ['k']
param_map[powerlaw] = ['a']
param_map[powerlognorm] = ['c', 's']
param_map[powernorm] = ['c']
param_map[rdist] = ['c']
param_map[rayleigh] = []
param_map[rice] = ['b']
param_map[recipinvgauss] = ['mu']
param_map[semicircular] = []
param_map[skewnorm] = ['a']
param_map[t] = ['df']
param_map[trapezoid] = ['c', 'd']
param_map[triang] = ['c']
param_map[truncexpon] = ['b']
param_map[truncnorm] = ['a', 'b']
param_map[tukeylambda] = ['lambda']
param_map[uniform] = []
param_map[vonmises] = ['k']
param_map[wald] = []
param_map[weibull_min] = ['c']
param_map[weibull_max] = ['c']
param_map[wrapcauchy] = ['c']
