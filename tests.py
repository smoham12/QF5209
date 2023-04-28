import unittest
from  closedform import bs_closedform, OptType, Metric

class TestQF5209(unittest.TestCase):
    
    def test_otm_call(self):
        result = bs_closedform(OptType.CALL, 2.0, 100.0, 110.0, 0.15, 0.05, Metric.PRICE)
        self.assertAlmostEqual(result, 8.6632353, places=7)
        
    def test_otm_put(self):
        result = bs_closedform(OptType.PUT, 2.0, 100.0, 90.0, 0.15, 0.05, Metric.PRICE)
        self.assertAlmostEqual(result, 1.688280, places=7)
        
        

if __name__ == "__main__":
    unittest.main()