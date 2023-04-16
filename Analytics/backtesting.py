import pandas as pd
import numpy as np
def calculate_profit(df_input, long_call = True, short_call = True, long_put = True, short_put = True, deviation = float('inf'))->pd.DataFrame:
    '''
    Calculate profit/loss of a long/short call/put option
    ======================
    Parameters:
    df_input: dataframe
        The dataframe containing the Call and Put price, strike price, underlying pice on expiry date
    long_call: boolean
        True if allow long call option
    short_call: boolean
        True if allow short call option
    long_put: boolean
        True if allow long put option
    short_put: boolean
        True if allow short put option
    deviation: float
        The deviation of the price from the strike price to allow long/short call/put option

    ======================

    Returns:
    df_input: dataframe
        The dataframe containing new columns of:
            LONG_CALL: 1 if long call, -1 if short call, 0 if not allowed
            LONG_PUT: 1 if long put, -1 if short put, 0 if not allowed
            PROFIT_LOSS_ON_PURCHASE_CALL: profit/loss on purchase of call option when before expiry
            PROFIT_LOSS_ON_PURCHASE_PUT: profit/loss on purchase of put option when before expiry
            PROFIT_LOSS_ON_PURCHASE: profit/loss on purchase of call/put option when before expiry
            PROFIT_LOSS_ON_SALE_CALL: profit/loss on sale of call option on expiry
            PROFIT_LOSS_ON_SALE_PUT: profit/loss on sale of put option on expiry
            PROFIT_LOSS_ON_SALE: profit/loss on sale of call/put option on expiry
            PROFIT_LOSS_CALL: profit/loss of call option
            PROFIT_LOSS_PUT: profit/loss of put option
            PROFIT_LOSS: profit/loss of call/put option combined

    '''
    long_call = 1 if long_call else 0
    short_call = -1 if short_call else 0
    long_put = 1 if long_put else 0
    short_put = -1 if short_put else 0
    
    # df_input['LONG_CALL'] = np.where(df_input['CALL'] > df_input['C_PRICE'], long_call, short_call)
    # df_input['LONG_PUT'] = np.where(df_input['PUT'] > df_input['P_PRICE'], long_put, short_put)
    dcall = (df_input['CALL'] - df_input['C_PRICE'])/df_input['C_PRICE']
    dput = (df_input['PUT'] - df_input['P_PRICE'])/df_input['P_PRICE']

    df_input['LONG_CALL'] = np.where(dcall > 0, np.where(dcall <= deviation, long_call, 0), np.where(dcall >= -deviation, short_call, 0))
    df_input['LONG_PUT'] = np.where(dput > 0, np.where(dput <= deviation, long_put, 0), np.where(dput >= -deviation, short_put, 0))


    df_input['PROFIT_LOSS_ON_PURCHASE_CALL'] = -(df_input['LONG_CALL']*df_input['C_PRICE'])
    df_input['PROFIT_LOSS_ON_PURCHASE_PUT'] = -(df_input['LONG_PUT']*df_input['P_PRICE'])
    df_input['PROFIT_LOSS_ON_PURCHASE'] = df_input['PROFIT_LOSS_ON_PURCHASE_CALL'] + df_input['PROFIT_LOSS_ON_PURCHASE_PUT']
    df_input['PROFIT_LOSS_ON_SALE_CALL'] = (df_input['LONG_CALL']*np.maximum(df_input['UNDERLYING_PRICE_EXPIRE'] - df_input['STRIKE'], 0))
    df_input['PROFIT_LOSS_ON_SALE_PUT'] = (df_input['LONG_PUT']*np.maximum(df_input['STRIKE'] - df_input['UNDERLYING_PRICE_EXPIRE'], 0))
    df_input['PROFIT_LOSS_ON_SALE'] = df_input['PROFIT_LOSS_ON_SALE_CALL'] + df_input['PROFIT_LOSS_ON_SALE_PUT']
    df_input['PROFIT_LOSS_CALL'] = df_input['PROFIT_LOSS_ON_SALE_CALL'] + df_input['PROFIT_LOSS_ON_PURCHASE_CALL']
    df_input['PROFIT_LOSS_PUT'] = df_input['PROFIT_LOSS_ON_SALE_PUT'] + df_input['PROFIT_LOSS_ON_PURCHASE_PUT']
    df_input['PROFIT_LOSS'] = df_input['PROFIT_LOSS_ON_SALE'] + df_input['PROFIT_LOSS_ON_PURCHASE']

    return df_input


def max_drawdown(return_series):
    comp_ret = (return_series+1).cumprod()
    peak = comp_ret.expanding(min_periods=1).max()
    dd = (comp_ret/peak)-1
    return dd.min()

def sharpe_ratio(return_series, rf, N=252):
    mean = return_series.mean() * N -rf
    sigma = return_series.std() * np.sqrt(N)
    return mean / sigma

def calmars_ratio(return_series, rf, N=252):
    mean = return_series.mean() * N -rf
    dd = max_drawdown(return_series)
    return mean / abs(dd)