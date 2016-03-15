
import numpy as np
from scipy.stats import sem


class Paths(object):
    
    def __init__(self,S0,r,sigma,T,nsteps,npaths):
        self.S0=S0
        self.r=r
        self.sigma=sigma
        self.T=T
        self.nsteps=nsteps
        self.npaths=npaths
        self.dt=T/nsteps
        self.time=np.linspace(0,T,nsteps)
        self.dW=np.sqrt(self.dt)
        self.randoms=np.random.normal(0,1,npaths*(nsteps-1))
        self.randoms.shape=[npaths,nsteps-1]
        
        paths=np.zeros(shape=(npaths,nsteps))
        # all paths start at S0
        paths[:,0]=S0
        
        for i in range(nsteps-1):
            paths[:,i+1]=paths[:,i]*np.exp( (self.r-.5*self.sigma**2)*self.dt + self.sigma*self.dW*self.randoms[:,i]) 
        self.paths=paths
        
    def get_paths(self):
        return self.paths
    
    def get_timeline(self):
        return self.time
    
    def get_path_final_position(self):
        return self.paths[:,-1]
    
    

    
def European(S0,K,r,sigma,T,is_call=True,size=100):
    ''' Calculates the European Call Price by Monte Carlo. A bit trivial in that the final price distribution
    is sampled from lognormal instead of evolving on a stochastic path.
    
    Pricing is evaluated by risk neutral means using the bank account as numeraire.
    '''
    S,K,r,sigma,T=map(float,[S,K,r,sigma,T])
    
    # prepapre the mean and standard deviation of lognormal from those of the interest rates
    mean_lognormal=(r-.5*sigma**2)*(T)
    sigma_lognormal=sigma*np.sqrt(T)
    
    # using these to get the final distribution of stock prices
    random_final_stock_prices=S*np.random.lognormal(mean_lognormal,sigma_lognormal,size)
    
    # get the final payoffs by taking e^{-r(T-t)} max(S-K,0)
    zeros=np.zeros_like(random_final_stock_prices)
    if is_call:
        payoff=random_final_stock_prices-K
    else:
        payoff=K-random_final_stock_prices
    payoff_final=np.exp(-r *(T-t))*np.where(payoff>zeros,payoff,zeros)
    
    # return the mean and the standard error of the mean (using scipy.stats.sem    # return the mean and the standard error of the mean (using scipy.stats.sem)
    return((payoff_final.mean(),sem(payoff_final)))




def European_Monte_Carlo(S,K,r,sigma,T,is_call=True,nsteps=1000,ntrials=10000):
    ''' Calculates the European Call Price by Monte Carlo generation of paths. '''
    S,K,r,sigma,T=map(float,[S,K,r,sigma,T])
    
    # generate random paths and use the final positions
    paths=Paths(S,r,sigma,T,nsteps,ntrials)
    random_final_stock_prices=paths.get_path_final_position()
    
    # get the final payoffs by taking e^{-r(T-t)} max(S-K,0)
    zeros=np.zeros_like(random_final_stock_prices)
    if is_call:
        payoff=random_final_stock_prices-K
    else:
        payoff=K-random_final_stock_prices
    payoff_final=np.exp(-r *(T))*np.where(payoff>zeros,payoff,zeros)
    
    # return the mean and the standard error of the mean (using scipy.stats.sem)
    return((payoff_final.mean(),sem(payoff_final)))



def Barrier_Out_Monte_Carlo(S,K,r,T,sigma,B,is_call=True,down_and_out=True,nsteps=1000,ntrials=10000):
    ''' Calculates the Barier Call Price by Monte Carlo. '''
    S,K,r,sigma,T=map(float,[S,K,r,sigma,T])
    
    # generate random paths and use the final positions
    paths=Paths(S,r,sigma,T,nsteps,ntrials)
    random_stock_paths=paths.get_paths()
    
    # should I just choose the ensemble to have paths that stayed below the barrier (and thus affect the measure)
    # or should I make the payoff for such paths zero?
    # I will do the former as I can understand the condition to mean the call is worth only if the price is above
    # a cutoff on the final day AND stays below another cutoff all the while. Otherwise its zero.
    
    if down_and_out:
        mask=random_stock_paths.min(1)<B
    else:
        mask=random_stock_paths.max(1)>B
    
    # select paths that stayed below barrier
    #random_stock_paths=random_stock_paths[mask]
    
    random_final_stock_prices=random_stock_paths[:,-1]
    
    # get the final payoffs by taking e^{-r(T-t)} max(S-K,0)
    zeros=np.zeros_like(random_final_stock_prices)
    if is_call:
        payoff=random_final_stock_prices-K
    else:
        payoff=K-random_final_stock_prices
    payoff[mask]=0.0
    payoff_final=np.exp(-r *(T))*np.where(payoff>zeros,payoff,zeros)
    
    
    # return the mean and the standard error of the mean (using scipy.stats.sem)
    return((payoff_final.mean(),sem(payoff_final)))




