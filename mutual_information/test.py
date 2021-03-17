import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
from scipy.stats import norm, entropy
import scipy.stats as ss
from sklearn.model_selection import KFold

#######################################

number_bits=2
number_classes=2**number_bits #the total number of values taken by the target intermediate

#setting the probability of the key
p_k= np.ones(number_classes, dtype=np.float64)
p_k/=number_classes


#defining the values for p(l|k), for the 4 different values of k
norm_params = np.array([[0, 0.3],[0.2,0.6], [-0.5, 0.1], [1, 2.8]])

#######################################

def measure_data(p_k,norm_params,number_samples=100):
    """ 
    p_k = discrete probability distribution if K
    norm_params = parameters of the true distributions
    number_samples = number of samples for each class of K. This corresponds to n^k_p

    returns leakage samples correponding to the target intermediate K and norm_params
    """
    data = {}
    for k, _ in enumerate(p_k):
        data[k]= ss.norm.rvs(*(norm_params[k]),size=number_samples)
    return data


#######################################

def visualize_distribution_points(data_dictionary, b='auto'):
    """
    plot the histogram of the elements in the lists
    as a function of the key values
    
    data_dictionary =  dictionary of lists, the key is the value of the keys and values are the samples l
                    = k: [l_0,l_1,....l_n]
    
    """
    for k in data_dictionary:

        plt.hist(data_dictionary[k], bins=b,density=True,alpha = 0.5,label='$k = %d$'%k)
    plt.xlabel("$p(l)$")
    plt.ylabel("$pr(l|k)$")
    plt.legend()
    plt.show()

#true_data=measure_data(p_k, norm_params)
#visualize_distribution_points(true_data)

#######################################

def print_format(l, cont=False):
    x = str(len(l))
    if type(l[0]) in [list, np.ndarray]:
        x = "{} x {}".format(x, print_format(l[0], True))

    if cont == False:
        print("[{}]".format(x))
    else:
        return x



def information(p_k,data,model):
    """
    implements I(K;L)
    
    p_k = the distribution of the sensitive variable K
    data = the samples we 'measured'. It its the n^k_p samples from p(l|k)
    model = the estimated model \hat{p}(l|k).

    returns an estimated of mutual information
    """
    N_k = len(p_k)              #N_k is the number of possible values for $K$
    acc = entropy(p_k,base=2)   #we initialize the value with H(K)
    acc2 = entropy(p_k,base=2)   #we initialize the value with H(K)
    for k in range(N_k):
        l = data[k]
        p_l_k = np.zeros((N_k,len(l)))
        for k_star in range(N_k):
            a = ss.norm.pdf(l,*(model[k_star]))
            p_l_k[k_star,:] = a
        p_l=np.sum(p_k*(p_l_k).T,axis=1)
        p_k_l =  p_k[k]*p_l_k[k,:]/ p_l
        acc += p_k[k] * np.mean(np.where(p_k_l != 0, np.log2(p_k_l), 0))

    return acc

import statsmodels.api as sm

data=measure_data(p_k, norm_params, number_samples=1000)
MI = information(p_k,data,norm_params)
print("MI is %f"%(MI))
