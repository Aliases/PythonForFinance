import numpy as np

from scipy.stats import norm

def d1(S,K,r,T,sigma):
    return (np.log(S/K)+(T)*(r+sigma**2/2))/(sigma*np.sqrt(T))

def d2(S,K,r,T,sigma):
    return (np.log(S/K)+(T)*(r-sigma**2/2))/(sigma*np.sqrt(T))



def h1(S,K,r,T,sigma,B):
    return (np.log(B**2/(S*K))+(T)*(r+sigma**2/2))/(sigma*np.sqrt(T))

def h2(S,K,r,T,sigma,B):
    return (np.log(B**2/(S*K))+(T)*(r-sigma**2/2))/(sigma*np.sqrt(T))


def EuOption(S,K,r,T,sigma,is_call=True):
    S,K,r,sigma,T=map(float,[S,K,r,sigma,T])
    D1=d1(S,K,r,T,sigma)
    D2=d2(S,K,r,T,sigma)
    if is_call:
        return S*norm.cdf(D1)-K*np.exp(-r*(T))*norm.cdf(D2)
    else:
        return K*np.exp(-r*(T))*norm.cdf(-D2)-S*norm.cdf(-D1)



def DownAndOut_call_option(S,K,r,T,sigma,B):
    S,K,B,r,sigma,T=map(float,[S,K,B,r,sigma,T])
    D1=d1(S,K,r,T,sigma)
    D2=d2(S,K,r,T,sigma)
    H1=h1(S,K,r,T,sigma,B)
    H2=h2(S,K,r,T,sigma,B)
    return S*( norm.cdf(D1) -(B/S)**(1+2*r/sigma**2)*norm.cdf(H1))-K*np.exp(-r*(T))*(norm.cdf(D2) - (B/S)**(-1+2*r/sigma**2)*norm.cdf(H2))


def UpAndOut_put_option(S,K,r,T,sigma,B):
    S,K,B,r,sigma,T=map(float,[S,K,B,r,sigma,T])
    D1=d1(S,K,r,T,sigma)
    D2=d2(S,K,r,T,sigma)
    H1=h1(S,K,r,T,sigma,B)
    H2=h2(S,K,r,T,sigma,B)
    return -S*( norm.cdf(-D1) -(B/S)**(1+2*r/sigma**2)*norm.cdf(-H1))+K*np.exp(-r*(T))*(norm.cdf(-D2) - (B/S)**(-1+2*r/sigma**2)*norm.cdf(-H2))


def UpAndOut_call_option(S,K,r,T,sigma,B):
    S,K,B,r,sigma,T=map(float,[S,K,B,r,sigma,T])
    D1=d1(S,K,r,T,sigma)
    D1KeqB=d1(S,B,r,T,sigma)
    D2=d2(S,K,r,T,sigma)
    D2KeqB=d2(S,B,r,T,sigma)
    H1=h1(S,K,r,T,sigma,B)
    H1KeqB=h1(S,B,r,T,sigma,B)
    H2=h2(S,K,r,T,sigma,B)
    H2KeqB=h2(S,B,r,T,sigma,B)
    
    return S*( (norm.cdf(D1)-norm.cdf(D1KeqB)) +(B/S)**(1+2*r/sigma**2)*(norm.cdf(-H1) -norm.cdf(-H1KeqB)))-K*np.exp(-r*(T))*((norm.cdf(D2)-norm.cdf(D2KeqB)) + (B/S)**(-1+2*r/sigma**2)*(norm.cdf(-H2)- norm.cdf(-H2KeqB)))


def DownAndOut_put_option(S,K,r,T,sigma,B):
    S,K,B,r,sigma,T=map(float,[S,K,B,r,sigma,T])
    D1=d1(S,K,r,T,sigma)
    D1KeqB=d1(S,B,r,T,sigma)
    D2=d2(S,K,r,T,sigma)
    D2KeqB=d2(S,B,r,T,sigma)
    H1=h1(S,K,r,T,sigma,B)
    H1KeqB=h1(S,B,r,T,sigma,B)
    H2=h2(S,K,r,T,sigma,B)
    H2KeqB=h2(S,B,r,T,sigma,B)
    
    return -S*( (norm.cdf(-D1)-norm.cdf(-D1KeqB)) +(B/S)**(1+2*r/sigma**2)*(norm.cdf(H1) -norm.cdf(H1KeqB)))+K*np.exp(-r*(T))*((norm.cdf(-D2)-norm.cdf(-D2KeqB)) + (B/S)**(-1+2*r/sigma**2)*(norm.cdf(H2)- norm.cdf(H2KeqB)))

