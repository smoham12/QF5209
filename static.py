from enum import Enum

class OptType(Enum):
    CALL = 1
    PUT = 2
    
class Metric(Enum):
    PRICE = 1
    DELTA = 2
