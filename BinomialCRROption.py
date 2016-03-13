from BinomialTreeOption import BinomialTreeOption
import math

class BinomialCRROption(BinomialTreeOption):
       
    def __setup_parameters__(self):
        self.u = math.exp(self.sigma * math.sqrt(self.dt))
        self.d = 1./self.u
        self.qu = (math.exp((self.r-self.div)*self.dt) -
                      self.d)/(self.u-self.d)
        self.qd = 1-self.qu   