import math

class StockOption(object):
    
    def __init__(self,S0,K,r,T,N,params):
        self.S0=S0
        self.K=K
        self.r=r
        self.T=T
        self.N=max(1,N)
        self.STs=None
        
        self.pu=params.get("pu",0)
        self.pd=params.get("pd",0)
        self.div=params.get("div",0)
        self.sigma=params.get("sigma",0)
        self.is_call=params.get("is_call",True)
        self.is_european=params.get("is_eu",True)
        
        self.dt=T/float(N)
        self.df=math.exp(-(r-self.div)*self.dt)
        
