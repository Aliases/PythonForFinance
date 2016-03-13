from StockOption import StockOption

import math
import numpy as np

class BinomialEuropeanOption(StockOption):
    
    # overloaded constructor. calls the parent class constructor first
    def __init__(self,S0,K,r,T,N,params):
        StockOption.__init__(self,S0,K,r,T,N,params)
        self.__setup_parameters__() # setup the parameters like number of nodes and risk neutral probabilities
        self._initialize_stock_price_tree_() # calculate the final stock prices
        self.price_of_option=self.__begin_tree_traversal__()[0]  # calculate payoffs at all nodes and return the payoff atthe first node
    
    # function used by constructor to setup relevant parameters
    def __setup_parameters__(self):
        self.M=self.N+1
        self.u=1+self.pu
        self.d=1-self.pd
        self.qu = (math.exp((self.r-self.div)*self.dt) -
                      self.d) / (self.u-self.d)
        self.qd=1-self.qu
        
    # set the stock prices at the final nodes
    def _initialize_stock_price_tree_(self):
        self.STs=np.zeros(self.M)
        for i in range(self.M):
            self.STs[i]=self.S0*(self.u**(self.N-i))*(self.d**i)
    
    # calculates the payoffs at the final nodes        
    def _intialize_payoffs_tree_(self):
        
        payoffs = np.maximum(
               0, (self.STs-self.K) if self.is_call
               else(self.K-self.STs))
        return payoffs
    
    # calculates the payoffs at increasingly higher nodes while retaining only the current values.
    # moreover only the components at the top of M+1 dimensional list is relevant
    # returns the payoff at the first node, i.e. the price of the option.
    def _traverse_tree_(self,payoffs):
        for i in range(self.N):
            payoffs=(payoffs[:-1]*self.qu + payoffs[1:]*self.qd)*self.df
            
        return payoffs
    
    # function to initialize and calculate all payoffs including the final one
    def __begin_tree_traversal__(self):
        payoffs=self._intialize_payoffs_tree_()
        return self._traverse_tree_(payoffs)
    
    def price(self):
        return self.price_of_option