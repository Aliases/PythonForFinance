import numpy as np


def EuOption(S,K,r,T,sigma,is_call=True):
    S,K,r,sigma,T=map(float,[S,K,r,sigma,T])
    d1=(np.log(S/K)+(T)*(r+sigma**2/2))/(sigma*np.sqrt(T))
    d2=(np.log(S/K)+(T)*(r-sigma**2/2))/(sigma*np.sqrt(T))
    if is_call:
        return S*norm.cdf(d1)-K*np.exp(-r*(T))*norm.cdf(d2)
    else:
        return K*np.exp(-r*(T))*norm.cdf(-d2)-S*norm.cdf(-d1)



def DownAndOut_call_option(S,K,r,T,sigma,B):
    S,K,B,r,sigma,T=map(float,[S,K,B,r,sigma,T])
    d1=(np.log(S/K)+(T)*(r+sigma**2/2))/(sigma*np.sqrt(T))
    d2=(np.log(S/K)+(T)*(r-sigma**2/2))/(sigma*np.sqrt(T))
    h1=(np.log(B**2/(S*K))+(T)*(r+sigma**2/2))/(sigma*np.sqrt(T))
    h2=(np.log(B**2/(S*K))+(T)*(r-sigma**2/2))/(sigma*np.sqrt(T))
    return S*( norm.cdf(d1) -(B/S)**(1+2*r/sigma**2)*norm.cdf(h1))-K*np.exp(-r*(T))*(norm.cdf(d2) - (B/S)**(-1+2*r/sigma**2)*norm.cdf(h2))


def UpAndOut_put_option(S,K,r,T,sigma,B):
    S,K,B,r,sigma,T=map(float,[S,K,B,r,sigma,T])
    d1=(np.log(S/K)+(T)*(r+sigma**2/2))/(sigma*np.sqrt(T))
    d2=(np.log(S/K)+(T)*(r-sigma**2/2))/(sigma*np.sqrt(T))
    h1=(np.log(B**2/(S*K))+(T)*(r+sigma**2/2))/(sigma*np.sqrt(T))
    h2=(np.log(B**2/(S*K))+(T)*(r-sigma**2/2))/(sigma*np.sqrt(T))
    return -S*( norm.cdf(-d1) -(B/S)**(1+2*r/sigma**2)*norm.cdf(-h1))+K*np.exp(-r*(T))*(norm.cdf(-d2) - (B/S)**(-1+2*r/sigma**2)*norm.cdf(-h2))









        
        


    










