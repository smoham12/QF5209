from math import log, sqrt, exp, erf
from scipy.stats import norm
from static import OptType, Metric, VanillaOption, ZeroCurve


def bs_closedform(opt: VanillaOption,
                asset: float,
                vol: float,
                zc: ZeroCurve,
                metric: Metric,
                ) -> float :    
    try:
        strike: float = opt.strike
        optType: OptType = opt.optType
        texp: float = opt.expiry
        
        df: float = zc.df(0, texp)
        rt: float = zc.rt(0, texp)
        
        sign: int = 1 if optType == OptType.CALL else -1
            
        if asset <= 0.0 or strike <= 0.0:
            raise ValueError("The distribution is lognormal and can not have non positive value for strike and asset.") 
        
        if vol < 0.0:
            raise ValueError("The standard deviation of the distribution must not be negative.") 
        
        stdev: float = vol*sqrt(texp)
        d1: float = ( log(asset / strike) + rt + 0.5*vol*vol*texp ) / stdev
        d2: float = d1 - stdev
        
        if metric == Metric.PRICE:
            return sign * ( asset*norm.cdf(sign*d1) - strike*df*norm.cdf(sign*d2) )
        elif metric == Metric.DELTA:
            return sign * norm.cdf(sign*d1)
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    option = VanillaOption(OptType.PUT, 2.0, 110.0)
    zc = ZeroCurve(0.05)
    rslt = bs_closedform(option, 100.0, 0.3, zc, Metric.PRICE)
    print(rslt)
    rslt = bs_closedform(option, 100.0, 0.3, zc, Metric.DELTA)
    print(rslt)