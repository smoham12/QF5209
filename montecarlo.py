from math import sqrt, exp
from scipy.stats import norm
import numpy as np
from static import OptType, Metric
from closedform import bs_closedform
import matplotlib.pyplot as plt

np.random.seed(42)

def bs_mc(optType: OptType,
            texp: float,
            asset: float,
            strike: float,
            vol: float,
            disc: float,
            metric: Metric,
            nbpaths: int,
            ) -> float :
    
    try:
        if optType == OptType.CALL:
            sign = 1
        elif optType == OptType.PUT:
            sign = -1
        else:
            raise ValueError("Invalid Option Type. Must be <OptType.CALL> or <OptType.PUT>.")
        
        if asset <= 0.0 or strike <= 0.0:
            raise ValueError("The distribution is lognormal and can not have non positive value for strike and asset.") 
        
        if vol < 0.0 or texp < 0.0:
            raise ValueError("The standard deviation of the distribution must not be negative.") 
        
        pv = 0
        delta = 0
        for p in range(nbpaths):
            z = np.random.normal()
            asset_T = asset * exp( (disc-0.5*vol*vol)*texp + vol*sqrt(texp)*z )
            payoff_T = max( sign*(asset_T - strike), 0.0)
            delta_T = sign*exp( (disc - 0.5*vol*vol)*texp + vol*sqrt(texp)*z ) if sign*(asset_T - strike) > 0.0 else 0.0
            pv +=  payoff_T
            delta += delta_T
            
        pv = pv*exp(-disc*texp) / nbpaths
        delta = delta*exp(-disc*texp) / nbpaths
        
        if metric == Metric.PRICE:
            return pv
        elif metric == Metric.DELTA:
            return delta
        
    except Exception as e:
        print(e)

def bs_qmc(optType: OptType,
            texp: float,
            asset: float,
            strike: float,
            vol: float,
            disc: float,
            metric: Metric,
            nbpaths: int,
            ) -> float :
    
    try:
        if optType == OptType.CALL:
            sign = 1
        elif optType == OptType.PUT:
            sign = -1
        else:
            raise ValueError("Invalid Option Type. Must be <OptType.CALL> or <OptType.PUT>.")
        
        if asset <= 0.0 or strike <= 0.0:
            raise ValueError("The distribution is lognormal and can not have non positive value for strike and asset.") 
        
        if vol < 0.0 or texp < 0.0:
            raise ValueError("The standard deviation of the distribution must not be negative.") 
        
        n = nbpaths + 2
        limit = 7.0
        width = (limit - -limit) / (nbpaths + 1)        
        pv = 0
        delta = 0        
        grid = np.linspace(-limit, limit, n)
        pdf = norm.pdf(grid)
        
        for i in range(n):
            asset_T = asset * exp( (disc-0.5*vol*vol)*texp + vol*sqrt(texp)*grid[i] )
            payoff_T = max( sign*(asset_T - strike), 0.0)
            delta_T = sign*exp( (disc - 0.5*vol*vol)*texp + vol*sqrt(texp)*grid[i] ) if sign*(asset_T - strike) > 0.0 else 0.0
            pv +=  payoff_T * pdf[i]
            delta += delta_T * pdf[i]
        
        pv = pv*exp(-disc*texp) * width
        delta = delta*exp(-disc*texp) * width
        
        if metric == Metric.PRICE:
            return pv
        elif metric == Metric.DELTA:
            return delta
        
    except Exception as e:
        print(e)
        
def plotConvergence(opType, T, S, K, v, r):
    
    paths = [ 200*i for i in range (1,5)]
    mc = []
    mcq = []
    
    
    target = bs_closedform(opType, T, S, K, v, r, Metric.PRICE)
    for p in paths:
        mc.append( ( bs_mc(opType, T, S, K, v, r, Metric.PRICE, p) - target ) / target )
        mcq.append( ( bs_qmc(opType, T, S, K, v, r, Metric.PRICE, p) - target ) / target )
        
    
    plt.plot(paths, mc, label="mc")
    plt.plot(paths, mcq, label="mcq")
    plt.xlabel("Number of Points")
    plt.xlabel("Convergence")
    leg = plt.legend(loc='upper center')
    plt.show()
    
if __name__ == "__main__":
    
    # S = 100
    # K = 130
    # T = 2.0
    # v = 0.15
    # r = 0.05
    # opType = OptType.CALL
    
    # plotConvergence(opType, T, S, K, v, r)
    
    
    nbpaths = 500
    S = 100
    K = 110
    T = 2.0
    v = 0.15
    r = 0.05
    opType = OptType.CALL
    
    rslt = bs_mc(opType, T, S, K, v, r, Metric.PRICE, nbpaths)
    print(rslt)
    rslt = bs_mc(opType, T, S, K, v, r, Metric.DELTA, nbpaths)
    print(rslt)
    rslt = bs_qmc(opType, T, S, K, v, r, Metric.PRICE, nbpaths)
    print(rslt)
    rslt = bs_qmc(opType, T, S, K, v, r, Metric.DELTA, nbpaths)
    print(rslt)
    rslt = bs_closedform(opType, T, S, K, v, r, Metric.PRICE)
    print(rslt)
    rslt = bs_closedform(opType, T, S, K, v, r, Metric.DELTA)
    print(rslt)