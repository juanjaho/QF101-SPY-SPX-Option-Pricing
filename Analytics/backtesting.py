import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#create a backtesting function that takes in data frame with option prices and a column with model optio price
# buy the option if the model price is less than the market price
# short the option if the model price is greater than the market price
def backtest(df, model_price_col):
    #create a new column that is the difference between the model price and the market price
    df['diff'] = df[model_price_col] - df['price']
    #create a new column that is the difference between the model price and the market price
    df['position'] = np.where(df['diff'] < 0, 1, -1)
    #create a new column that is the difference between the model price and the market price
    df['pnl'] = df['diff'] * df['position']
    #create a new column that is the difference between the model price and the market price
    df['cum_pnl'] = df['pnl'].cumsum()
    #create a new column that is the difference between the model price and the market price
    df['cum_ret'] = df['cum_pnl'] / df['price'].iloc[0]
    #create a new column that is the difference between the model price and the market price
    df['cum_ret'].plot()
    #create a new column that is the difference between the model price and the market price
    plt.show()
    #create a new column that is the difference between the model price and the market price
    return df
    