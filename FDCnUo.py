import numpy as np

from FDCnEu import FDCnEu

class FDCnUo(FDCnEu):
    
    def __init__(self,S0,K,r,T,sigma,Sbarrier,Smax,M,N,is_call=True):
        # We just replace Smax by Sbarrier
        Smax=Sbarrier
        super(FDCnUo, self).__init__(
               S0, K, r, T, sigma, Smax, M, N, is_call)
        
    def _setup_boundary_conditions_(self):
        FDCnEu._setup_boundary_conditions_(self)
        # Since this is a down and out option the payoff on the lowest level of the grid should be zero corresponding to that boundary condition       
        self.grid[-1,:]=0.0
        
        
def main():
    S0,K,r,T,sigma,Sbarrier,Smax,M,N=50, 50, 0.1, 5./12., 0.4, 70, 200, 120, 500
    print "Demo with S0=%f,K=%f,r=%f,T=%f,sigma=%f,Sbarrier=%f,Smax=%f,M=%i,N=%i" % (S0,K,r,T,sigma,Sbarrier,Smax,M,N)
    call_option=FDCnUo(S0,K,r,T,sigma,Sbarrier,Smax,M,N)
    put_option=FDCnUo(S0,K,r,T,sigma,Sbarrier,Smax,M,N,False)
    
    
    print "*"*10, " results from analytical expressions ", "*"*10
    import AnalyticalFormulae
    print "Price from analytical expression for call is %f" % AnalyticalFormulae.UpAndOut_call_option(S0,K,r,T,sigma,Sbarrier)
    print "Price from analytical expression for put is %f" % AnalyticalFormulae.UpAndOut_put_option(S0,K,r,T,sigma,Sbarrier)


    print "*"*10, " results from numerical PDE ", "*"*10
    print "Price of call option is %f" % call_option.price()
    print "Price of put option is %f" % put_option.price()
    
    import MonteCarloMethods
    print "*"*10, " results from Monte Carlo ", "*"*10
    print "Price from analytical expression for call is %f +- %f" % MonteCarloMethods.Barrier_Out_Monte_Carlo(S0,K,r,T,sigma,Sbarrier,down_and_out=False,is_call=True,ntrials=50000)
    print "Price from analytical expression for put is %f +- %f" % MonteCarloMethods.Barrier_Out_Monte_Carlo(S0,K,r,T,sigma,Sbarrier,down_and_out=False,is_call=False,ntrials=50000)



if __name__ == "__main__":
    main()