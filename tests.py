import unittest
from math import exp

from static import OptType, Metric
from closedform import bs_closedform
from montecarlo import bs_mc, bs_qmc

class TestQF5209(unittest.TestCase):
    
    def test_closedform_otm_call(self):
        result = bs_closedform(OptType.CALL, 2.0, 100.0, 110.0, 0.15, 0.05, Metric.PRICE)
        self.assertAlmostEqual(result, 8.6632353, places=7)
        
    def test_closedform_otm_put(self):
        result = bs_closedform(OptType.PUT, 2.0, 100.0, 90.0, 0.15, 0.05, Metric.PRICE)
        self.assertAlmostEqual(result, 1.688280, places=7)
    
    def test_closedform_put_call_parity(self):
        S=100
        K=110
        T=3
        r=0.05
        vol=0.15
        
        call_pv = bs_closedform(OptType.CALL, T, S, K, vol, r, Metric.PRICE)
        put_pv = bs_closedform(OptType.PUT, T, S, K, vol, r, Metric.PRICE)
        
        self.assertAlmostEqual(call_pv - put_pv, S - K*exp(-r*T), places=7)
     
    def test_montecarlo_otm_call(self):
        S=100
        K=110
        T=2.0
        r=0.05
        vol=0.15
        opType = OptType.CALL
        
        call_closedform = bs_closedform(opType, T, S, K, vol, r, Metric.PRICE)
        call_mc = bs_mc(opType, T, S, K, vol, r, Metric.PRICE, 10000)
        call_qmc = bs_qmc(opType, T, S, K, vol, r, Metric.PRICE, 10000)
        self.assertAlmostEqual(call_qmc, call_closedform, places=5)   
        self.assertAlmostEqual(call_mc, 8.666161954306851, places=5)   
    

if __name__ == "__main__":
    unittest.main()