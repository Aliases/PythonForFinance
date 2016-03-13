from StockOption import StockOption

import math
import numpy as np

class BinomialTreeOption(StockOption):
    
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
        
    # set the stock prices at each node starting from the leftmost (ccurrent)
    def _initialize_stock_price_tree_(self):
        self.STs=[np.array([self.S0])]
        for i in range(self.N):
            prev_branches=self.STs[-1]
            st = np.concatenate((prev_branches*self.u,
                                    [prev_branches[-1]*self.d]))
            self.STs.append(st)
    
    # calculates the payoffs at the final nodes        
    def _intialize_payoffs_tree_(self):
        
        payoffs = np.maximum(
               0, (self.STs[self.N]-self.K) if self.is_call
               else(self.K-self.STs[self.N]))
        return payoffs
    
    # for a given node and payoffs calculated by risk neutral method from later nodes check of early excercise is better
    # by returning the maximum
    def __check_early_exercise__(self, payoffs, node):
        early_ex_payoff = (self.STs[node] - self.K) if self.is_call else (self.K - self.STs[node])
        return np.maximum(payoffs, early_ex_payoff)
    
    
    # calculates the payoffs going from later times to earlier ones. the values are NOT stored. the value at the earliers node
    # is returned
    def _traverse_tree_(self,payoffs):
        for i in reversed(range(self.N)):
            payoffs=(payoffs[:-1]*self.qu + payoffs[1:]*self.qd)*self.df
            
            if not self.is_european:
                payoffs = self.__check_early_exercise__(payoffs,i)
        return payoffs
    
    # function to initialize and calculate all payoffs including the final one
    def __begin_tree_traversal__(self):
        payoffs=self._intialize_payoffs_tree_()
        return self._traverse_tree_(payoffs)
    
    def price(self):
        return self.price_of_option