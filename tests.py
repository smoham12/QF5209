import unittest
from math import exp

from static import OptType, Metric, VanillaOption, ZeroCurve
from closedform import bs_closedform
from montecarlo import bs_mc, bs_qmc

class TestQF5209(unittest.TestCase):
    
    def test_closedform_otm_call(self):
        S=100
        K=110
        T=2.0
        r=0.05
        vol=0.15
        
        option = VanillaOption(OptType.CALL, T, K)
        zc = ZeroCurve(r)
        result = bs_closedform(option, S, vol, zc, Metric.PRICE)
        self.assertAlmostEqual(result, 8.6632353, places=7)
        
    def test_closedform_otm_put(self):
        S=100
        K=90
        T=2.0
        r=0.05
        vol=0.15
        
        option = VanillaOption(OptType.PUT, T, K)
        zc = ZeroCurve(r)
        result = bs_closedform(option, S, vol, zc, Metric.PRICE)
        self.assertAlmostEqual(result, 1.688280, places=7)
    
    def test_closedform_put_call_parity(self):
        S=100
        K=110
        T=3
        r=0.05
        vol=0.15
        
        optPut = VanillaOption(OptType.PUT, T, K)
        optCall = VanillaOption(OptType.CALL, T, K)
        zc = ZeroCurve(r)        
        call_pv = bs_closedform(optCall, S, vol, zc, Metric.PRICE)
        put_pv = bs_closedform(optPut, S, vol, zc, Metric.PRICE)
        
        self.assertAlmostEqual(call_pv - put_pv, S - K*exp(-r*T), places=7)
     
    def test_montecarlo_otm_call(self):
        S=100
        K=110
        T=2.0
        r=0.05
        vol=0.15
        opType = OptType.CALL
        
        option = VanillaOption(opType, T, K)
        zc = ZeroCurve(r)        
        call_closedform = bs_closedform(option, S, vol, zc, Metric.PRICE)
        call_mc = bs_mc(option, S, vol, zc, Metric.PRICE, 10000)
        call_qmc = bs_qmc(option, S, vol, zc, Metric.PRICE, 10000)
        self.assertAlmostEqual(call_qmc, call_closedform, places=5)   
        self.assertAlmostEqual(call_mc, 8.666161954306851, places=5)   
    

if __name__ == "__main__":
    unittest.main()