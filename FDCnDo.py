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
        