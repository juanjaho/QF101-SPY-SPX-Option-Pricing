import numpy as np


def binomial_model(N, S0, u, r, K):
    """
    N = number of binomial iterations
    S0 = initial stock price
    u = factor change of upstate
    r = risk free interest rate per annum
    K = strike price
    """
    d = 1 / u
    # p = (1 + r - d) / (u - d)
    p = (np.exp(r) - d) / (u - d)
    q = 1 - p

    # make stock price tree
    stock = np.zeros([N + 1, N + 1])
    for i in range(N + 1):
        for j in range(i + 1):
            stock[j, i] = S0 * (u ** (i - j)) * (d ** j)

    
    # Generate option prices recursively
    option = np.zeros([N + 1, N + 1])
    # call option
    option[:, N] = np.maximum(np.zeros(N + 1), (stock[:, N] - K))
    # put option
    # option[:, N] = np.maximum(np.zeros(N + 1), (K - stock[:, N]))
    for i in range(N - 1, -1, -1):
        for j in range(0, i + 1):
            option[j, i] = (
                #European  option
                np.exp(-r) * (p * option[j, i + 1] + q * option[j + 1, i + 1])

                #American call option
                # np.maximum(np.exp(-r) * (p * option[j, i + 1] + q * option[j + 1, i + 1]), (stock[j, i] - K))
                
                
            )
            
    return option


if __name__ == "__main__":
    print("Calculating example option price:")
    op_price = binomial_model(30, 20, 0.5, 10.25,8 )
    # print(op_price)

    # discount price to present value
    print("Present value of option price:")
    print(op_price[0, 0])
