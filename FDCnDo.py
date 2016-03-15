import numpy as np

from FDCnEu import FDCnEu

class FDCnDo(FDCnEu):
    
    def __init__(self,S0,K,r,T,sigma,Sbarrier,Smax,M,N,is_call=True):
        super(FDCnDo, self).__init__(
               S0, K, r, T, sigma, Smax, M, N, is_call)
        # The idea is to treat this just like a vanilla option with Sbarrier replacing S=0
        self.dS=(Smax-Sbarrier)/float(self.M)
        self.boundary_conds=np.linspace(Sbarrier,Smax,self.M+1)
        
        # The values of i have to be adjusted to go from Sbarrier to Smax
        self.i_values=np.array(map(lambda x: int(x),self.boundary_conds/self.dS))
        
    def _setup_boundary_conditions_(self):
        FDCnEu._setup_boundary_conditions_(self)
        # Since this is a down and out option the payoff on the lowest level of the grid should be zero corresponding to that boundary condition       
        self.grid[0,:]=0.0
        
        
def main():
    S0,K,r,T,sigma,Sbarrier,Smax,M,N=50, 50, 0.1, 5./12., 0.4, 40, 200, 120, 500
    print "Demo with S0=%f,K=%f,r=%f,T=%f,sigma=%f,Sbarrier=%f,Smax=%f,M=%i,N=%i" % (S0,K,r,T,sigma,Sbarrier,Smax,M,N)
    call_option=FDCnDo(S0,K,r,T,sigma,Sbarrier,Smax,M,N)
    put_option=FDCnDo(S0,K,r,T,sigma,Sbarrier,Smax,M,N,False)

    
    print "*"*10, " results from analytical expressions ", "*"*10
    import AnalyticalFormulae
    print "Price from analytical expression for call is %f" % AnalyticalFormulae.DownAndOut_call_option(S0,K,r,T,sigma,Sbarrier)
    print "Price from analytical expression for put is %f" % AnalyticalFormulae.DownAndOut_put_option(S0,K,r,T,sigma,Sbarrier)

    print "*"*10, " results from numerical PDE ", "*"*10
    print "Price of call option is %f" % call_option.price()
    print "Price of put option is %f" % put_option.price()
    
    
    import MonteCarloMethods
    print "*"*10, " results from Monte Carlo ", "*"*10
    print "Price from analytical expression for call is %f +- %f" % MonteCarloMethods.Barrier_Out_Monte_Carlo(S0,K,r,T,sigma,Sbarrier,down_and_out=True,is_call=True,ntrials=50000)
    print "Price from analytical expression for put is %f +- %f" % MonteCarloMethods.Barrier_Out_Monte_Carlo(S0,K,r,T,sigma,Sbarrier,down_and_out=True,is_call=False,ntrials=50000)


if __name__ == "__main__":
    main()