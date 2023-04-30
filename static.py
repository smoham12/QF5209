from enum import Enum
from math import exp, log

class OptType(Enum):
    CALL = 1
    PUT = 2
    
class Metric(Enum):
    PRICE = 1
    DELTA = 2

class VanillaOption:
    def __init__(self, type: OptType, t: float, k: float):
        if type != OptType.CALL and type != OptType.PUT:
            raise ValueError("Invalid Option Type. Must be <OptType.CALL> or <OptType.PUT>.")
        else:
            self.optType = type
            
        if t < 0.0:
            raise ValueError("Time to expiry must be non negative.") 
        else:
            self.expiry = t
        
        self.strike = k
        
        
class ZeroCurve:
    def __init__(self, r: float):
        self.discrate = r
        
    def df(self, t1: float, t2: float):
        r = self.discrate
        return exp(-r*t2) / exp(-r*t1)
    
    def rt(self, t1: float, t2: float):
        return -log(self.df(t1, t2))