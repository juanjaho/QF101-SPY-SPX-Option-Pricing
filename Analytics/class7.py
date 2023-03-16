import pandas as pd
import numpy as np
pvdata = pd.read_csv('./Analytics/pvdata.csv')
pvdata = pvdata[['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']]
pvdata['date'] = pd.to_datetime(pvdata['date'], format = "%Y%m%d")
tdate = pvdata['date'].copy(deep=True)
mindex = pd.MultiIndex.from_frame(pvdata[['ticker','date']])
pvdata.index = mindex
pvdata = pvdata[['close']]
r = pvdata.unstack(level = -1)
r = r.transpose()
r.index = sorted(list(set(tdate)))
r = r.tail(252*3)  ##use latest 3 years only, mainly to avoid time series with large number of NANs before


#####try naive mean variance optimizer
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import black_litterman, risk_models
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.black_litterman import BlackLittermanModel
import matplotlib.pyplot as plt

# mu = mean_historical_return(r)
S = CovarianceShrinkage(r['AA'],log_returns=True).ledoit_wolf()
print(np.sqrt(np.diag(S)))

log_returns = np.log(r['AA']).diff()
print(log_returns.std()*np.sqrt(252))
# ef = EfficientFrontier(mu, S)  # setup
# ef.max_sharpe()
# weights = ef.clean_weights()
# weights = pd.Series(weights)
# plt.plot(weights.sort_values().tail(20))  #just visualize 20 of the weights
# plt.show()

# #####black litterman
# mcap = pd.read_csv('marketcap_clean.csv')
# mcap.index = mcap['ticker']
# mcapdict = dict()
# for t in list(r.columns):
#     try:
#         mcapdict[t] = mcap.loc[mcap.index==t, :].values[0][1]
#     except:
#         mcapdict[t] = 1.0

# prior = black_litterman.market_implied_prior_returns(mcapdict, 2.0, S)

# viewdict = {"AAT": 0.10, "AA": 0.05} ##sample views
# bl = BlackLittermanModel(S, absolute_views = viewdict, pi = prior)
# rets = bl.bl_returns()
# ef = EfficientFrontier(rets, S)
# ef.max_sharpe()
# bl_weights = ef.clean_weights()
# bl_weights = pd.Series(bl_weights)
# plt.plot(bl_weights.sort_values().tail(20))  #just visualize 20 of the weights
# plt.show()