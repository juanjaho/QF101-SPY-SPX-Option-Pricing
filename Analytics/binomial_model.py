# Binomial model for option pricing

import numpy as np
import scipy.stats as ss

# the fuction should also account for dividends
def binomial_model(S0, K, T, r, sigma, N, 
                   option='call', div=0, 
                   european=True, method='crr'):
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
    method : string
        'crr' for Cox, Ross and Rubinstein
        'jr' for Jarrow and Rudd/equal probabilities 
    Returns
    =======
    value : float
        present value of the European option
    '''
    dt = T / N
    
    # calculate the risk-neutral probability
    if method == 'crr':
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp((r - div) * dt) - d) / (u - d)
    elif method == 'jr':
        u = np.exp((r-div-0.5*sigma**2)*dt+sigma*np.sqrt(dt))
        d = np.exp((r-div-0.5*sigma**2)*dt-sigma*np.sqrt(dt))
        p = 0.5
    else:
        raise ValueError('method not recognized')

    q = 1 - p

    # initialize terminal stock prices at maturity
    stock_prices = np.zeros((N + 1, N + 1))
    stock_prices[0, 0] = S0
    for i in range(1, N + 1):
        stock_prices[0, i] = stock_prices[0, i - 1] * u
        for j in range(1, i + 1):
            stock_prices[j, i] = stock_prices[j - 1, i - 1] * d

    # calculate option values at maturity
    option_values = np.zeros((N + 1, N + 1))
    if option == 'call':
        option_values[:, N] = np.maximum(stock_prices[:, N] - K, 0)
    else:
        option_values[:, N] = np.maximum(K - stock_prices[:, N], 0)

    # backward induction
    if european:
        for i in range(N - 1, -1, -1):
            for j in range(i + 1):
                option_values[j, i] = np.exp(-r * dt) * (p * option_values[j, i + 1] + q * option_values[j + 1, i + 1])
    else:
        if option == 'call':
            for i in range(N - 1, -1, -1):
                for j in range(i + 1):
                    option_values[j, i] = np.exp(-r * dt) * (p * option_values[j, i + 1] + q * option_values[j + 1, i + 1])
                    option_values[j, i] = np.maximum(option_values[j, i], stock_prices[j, i] - K)
        else:
            for i in range(N - 1, -1, -1):
                for j in range(i + 1):
                    option_values[j, i] = np.exp(-r * dt) * (p * option_values[j, i + 1] + q * option_values[j + 1, i + 1])
                    option_values[j, i] = np.maximum(option_values[j, i], K - stock_prices[j, i])
    
    return option_values[0, 0]



# Example
# S0 = 3246.23
# K = 2000
# T = 21/252
# r = 0.025
# div = 0.015
# sigma = 0.1498878078948466
# N = 21
# print(binomial_model(S0, K, T, r, sigma, N, option='call', div=div, european=True, method='crr'))
# print(binomial_model(S0, K, T, r, sigma, N, option='call', div=div, european=True, method='jr'))


