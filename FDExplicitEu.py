import numpy as np

from FiniteDifferences import FiniteDifferences

class FDExplicitEu(FiniteDifferences):
    
    def _setup_boundary_conditions_(self):
        if self.is_call:
            # recall self.boundary_conds contains all values of stocks possible
            # the next command gives final call values and is the final condition
            self.grid[:,-1]=np.maximum(self.boundary_conds-self.K,0)
        else:
            # recall self.boundary_conds contains all values of stocks possible
            # the next command gives final call values and is this the boundary condition at final time
            self.grid[:,-1]=np.maximum(self.K-self.boundary_conds,0)
            
        
        # the original code in the book uses
        #self.grid[-1,:-1]=(self.K-self.Smax)*np.exp(-self.r*self.dt*(self.N-self.j_values))
        # for upper boundary condition and maintaines zero for lower for call
        # and 
        #self.grid[0,:-1]=(self.K-self.Smax)*np.exp(-self.r*self.dt*(self.N-self.j_values))
        # for the lower boundary condition and maintains zero for the upper for put
        # I don't think the latter is correct
        
        
        # the following gives the boundary condition at the top and bottom row as the final values discounted
        self.grid[-1,:-1]=(self.grid[-1,-1] )*np.exp(-self.r*self.dt*(self.N-self.j_values))
        self.grid[0,:-1]=(self.grid[0,-1])*np.exp(-self.r*self.dt*(self.N-self.j_values))
            
    def _setup_coefficients_(self):
        self.a=0.5*self.dt*((self.sigma**2) * (self.i_values**2)-self.r*self.i_values)
        self.b=1-self.dt*((self.sigma**2) * (self.i_values**2)+self.r)
        self.c=0.5*self.dt*((self.sigma**2)* (self.i_values**2)+self.r*self.i_values)
        
    def _traverse_grid_(self):
        
        # The quoted out part is from the book and took 226 ms whereas the numpy vectorized method took 18 ms
        
        '''
        for j in reversed(self.j_values):
            for i in range(self.M)[2:]:
                self.grid[i,j]=self.a[i]*self.grid[i-1,j+1]+self.b[i]*self.grid[i,j+1]+self.c[i]*self.grid[i+1,j+1]
        
        '''
        
        for j in reversed(self.j_values):
            self.grid[2:-1,j]=self.a[2:]*self.grid[1:-2,j+1] +self.b[2:]*self.grid[2:-1,j+1]+self.c[2:]*self.grid[3:,j+1]
            