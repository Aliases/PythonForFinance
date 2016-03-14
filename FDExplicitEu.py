import numpy as np

from FiniteDifferences import FiniteDifferences

class FDExplicitEu(FiniteDifferences):
    
    def _setup_boundary_conditions_(self):
        if self.is_call:
            # recall self.boundary_conds contains all values of stocks possible
            # the next command gives final call values and is this the boundary condition at final time
            self.grid[:,-1]=np.maximum(self.boundary_conds-self.K,0)
            # the following gives the boundary condition at the top row that corresponds to maximum
            # value the stock can take. The price here is taken to be just the discounted price at the final time
            self.grid[-1,:-1]=(self.Smax-self.K)*np.exp(-self.r*self.dt*(self.N-self.j_values))
            # the boundary condition at the bottom is autmoatically consisten with the value at the final time i.e. 0
            # from the initialization of grid
            
        else:
            # recall self.boundary_conds contains all values of stocks possible
            # the next command gives final call values and is this the boundary condition at final time
            self.grid[:,-1]=np.maximum(self.K-self.boundary_conds,0)
            # the following gives the boundary condition at the bottom row that corresponds to minimum value the stock can take
           
            # *********** However it still uses Smax ********??????????
            #self.grid[0,:-1]=(self.K-self.Smax)*np.exp(-self.r*self.dt*(self.N-self.j_values))
            # I think thats a typo and it should be
            self.grid[0,:-1]=(self.K)*np.exp(-self.r*self.dt*(self.N-self.j_values))
            # to be consisten with final condition and Smin=0
            # The price has been discounted obviously
            
            # The top boundary is already 0 by the grid initialization and is consistent with the final condition at the
            # top boundary
            
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
            