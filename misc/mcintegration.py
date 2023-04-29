from math import sqrt, exp, pi
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


def norm_pdf(z: float):
    return 1 / sqrt(2 * pi) * exp( -0.5*z*z )

def trapeziumIntegration(n: int, low: float, high: float, func):
    step = (high - low)  / n
    nbSegments = n + 1
    
    prev = low
    a = func(prev)
    b = 0
    area = 0
    
    for i in range(nbSegments):
        b = func( prev + step )
        area += 0.5 * step * (a + b)
        
        a = b
        prev += step
        
    return area


def midpointIntegration(nbKnots: int, low: float, high: float, func):
    n = nbKnots + 2
    width = (high - low) / (nbKnots + 1)
    area = 0
    midpoint = low
    for i in range(n):
        area += func(midpoint)*width
        midpoint += width
        
    return area



def monteCarloIntegration(n: int, low: float, high: float, func):
    total = 0
    for i in range(n):
        u = np.random.uniform(low, high)
        total += func(u) * (high - low)
    
    average = total / n
    return average



def plotConvergence(low: float, high: float):
    # subproblems = [50, 100, 500, 1000, 5000, 10000]
    subproblems = [ 200*i for i in range (1,41)]
    mc = []
    mcq = []
    target = norm.cdf(high) - norm.cdf(low)
    for s in subproblems:
        mcq.append( ( midpointIntegration(s, low, high, norm_pdf) - target ) / target )
        mc.append( ( monteCarloIntegration(s, low, high, norm_pdf) - target ) / target )

    
    plt.plot(subproblems, mc, label="mc")
    plt.plot(subproblems, mcq, label="mcq")
    plt.xlabel("Number of Points")
    plt.xlabel("Convergence")
    leg = plt.legend(loc='upper center')
    plt.show()

# p = 10000
# rslt = trapeziumIntegration(p, -1.645, 1.645, norm_pdf)
# print(rslt)

# rslt = midpointIntegration(p, -1.645, 1.645, norm_pdf)
# print(rslt)

# rslt = monteCarloIntegration(10000, -1.645, 1.645, norm_pdf)
# print(rslt)
np.random.seed(42)
# plotConvergence(-1.645, 1.645)
plotConvergence(-1.645, 1.645)