# Trinomial model for option pricing

import numpy as np
import scipy.stats as ss
import pprint as pp
# the fuction should also account for dividends
def trinomial_model(S0, K, T, r, sigma, N, 
                   option='call', div=0, 
                   european=True):
    ''' Binomial model for option pricing.
    Parameters
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity (in year fractions)
    r : float
        constant risk-free short rate
    sigma : float
        volatility factor in diffusion term 
    N : int
        number of time intervals
    option : string
        type of the option to be valued ('call' or 'put')
    div : float
        annualized continuous dividend yield
    european : boolean
        True for European option valuation
        False for American option valuation
    Returns
    =======
    value : float
        present value of the European option
    '''
    dt = T / N
    
    # calculate the risk-neutral probability
    u = np.exp(sigma * np.sqrt(3*dt))
    d = 1 / u

    pu = np.sqrt(dt/(12*sigma**2))*(r-0.5*sigma**2)+1/6
    pd = -np.sqrt(dt/(12*sigma**2))*(r-0.5*sigma**2)+1/6
    pm = 2/3


    # initialize terminal stock prices at maturity for trinomial model
    stock_price = np.zeros((2*N+1, N+1))
    stock_price[N, 0:] = S0
    
    #fill up upper and lower diagonal
    for i in range(1, N+1):
        stock_price[N-i, i:] = stock_price[N-i+1, i-1]*u
        stock_price[N+i, i:] = stock_price[N+i-1, i-1]*d
        
    # calculate option values at maturity
    option_value = np.zeros((2*N+1, N+1))
    if option == 'call':
        option_value[:, N] = np.maximum(stock_price[:, N] - K, 0)
    else:
        option_value[:, N] = np.maximum(K - stock_price[:, N], 0)


    # backward induction
    if european:
        for i in range(N-1, -1, -1):
            for j in range(N-i, N+i+1):
                option_value[j, i] = np.exp(-r*dt)*(pu*option_value[j-1, i+1] + pm*option_value[j, i+1] + pd*option_value[j+1, i+1])
    else:
        if option == 'call':
            for i in range(N-1, -1, -1):
                for j in range(N-i, N+i+1):
                    option_value[j, i] = np.exp(-r*dt)*(pu*option_value[j-1, i+1] + pm*option_value[j, i+1] + pd*option_value[j+1, i+1])
                    option_value[j, i] = np.maximum(option_value[j, i], stock_price[j, i] - K)
        else:
            for i in range(N-1, -1, -1):
                for j in range(N-i, N+i+1):
                    option_value[j, i] = np.exp(-r*dt)*(pu*option_value[j-1, i+1] + pm*option_value[j, i+1] + pd*option_value[j+1, i+1])
                    option_value[j, i] = np.maximum(option_value[j, i], K - stock_price[j, i])

    return option_value[N, 0]




# Example
S0 = 100
K = 101
T = 1
r = 0.04
div = 0
sigma = 0.2
N = 3

# pp.pprint(trinomial_model(S0, K, T, r, sigma, N, option='call', div=div, european=True))
# pp.pprint(trinomial_model(S0, K, T, r, sigma, N, option='put', div=div, european=True))
# print(trinomial_model(S0, K, T, r, sigma, N, option='call', div=div, european=False))
# print(trinomial_model(S0, K, T, r, sigma, N, option='put', div=div, european=False))


