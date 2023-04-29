from math import log, sqrt, exp, erf
from scipy.stats import norm
from static import OptType, Metric


def bs_closedform(optType: OptType,
                texp: float,
                asset: float,
                strike: float,
                vol: float,
                disc: float,
                metric: Metric,
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
        
        stdev = vol*sqrt(texp)
        d1 = ( log(asset / strike) + (disc + 0.5*vol*vol)*texp ) / stdev
        d2 = d1 - stdev
        
        if metric == Metric.PRICE:
            return sign * ( asset*norm.cdf(sign*d1) - strike*exp(-disc*texp)*norm.cdf(sign*d2) )
        elif metric == Metric.DELTA:
            return sign * norm.cdf(sign*d1)
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    rslt = bs_closedform(OptType.PUT, 2.0, 100.0, 110.0, 0.3, 0.05, Metric.PRICE)
    print(rslt)
    rslt = bs_closedform(OptType.PUT, 2.0, 100.0, 110.0, 0.3, 0.05, Metric.DELTA)
    print(rslt)