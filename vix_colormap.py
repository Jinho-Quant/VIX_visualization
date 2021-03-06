# -*- coding: utf-8 -*-
"""VIX colormap.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Mwj3J_wpmDr06-ryT3FPmIKF9b4w7eEk
"""

##Datasourcing
from google.colab import drive
import numpy as np
import pandas as pd

##Alpha Vantage API Key
key = '0D6HAHFDZPJLAL0E'
return_horizon = 50

import requests

##S&P500, Nasdaq, Dow-Jones data (thru ETF)
##S&P500 - SPY
spyurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPY&outputsize=full&apikey=' + key
spyurldata = pd.DataFrame(requests.get(spyurl).json()['Time Series (Daily)']).transpose()
spyurldata.index = pd.to_datetime(spyurldata.index)
spy_price = spyurldata.astype(float)
spy_price = spy_price[::-1]
print(spy_price)

##Nasdaq 100  - QQQ
qqqurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=QQQ&outputsize=full&apikey=' + key
qqqurldata = pd.DataFrame(requests.get(qqqurl).json()['Time Series (Daily)']).transpose()
qqqurldata.index = pd.to_datetime(qqqurldata.index)
qqq_price = qqqurldata.astype(float)
qqq_price = qqq_price[::-1]
print(qqq_price)

##Dow Jones - DIA
diaurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=DIA&outputsize=full&apikey=' + key
diaurldata = pd.DataFrame(requests.get(diaurl).json()['Time Series (Daily)']).transpose()
diaurldata.index = pd.to_datetime(diaurldata.index)
dia_price = diaurldata.astype(float)
dia_price = dia_price[::-1]
print(dia_price)

##VIX index - VIXY
vixurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=VIXY&outputsize=full&apikey=' + key
vixurldata = pd.DataFrame(requests.get(vixurl).json()['Time Series (Daily)']).transpose()
vixurldata.index = pd.to_datetime(vixurldata.index)
vix_price = vixurldata.astype(float)
vix_price = vix_price[::-1]
print(vix_price)

##negative directional indicator for VIXY
negdiurl = 'https://www.alphavantage.co/query?function=MINUS_DI&symbol=VIXY&interval=daily&time_period='+str(return_horizon)+'&apikey=' + key
negdirdata = pd.DataFrame(requests.get(negdiurl).json()["Technical Analysis: MINUS_DI"]).transpose()
negdirdata.index = pd.to_datetime(negdirdata.index)
negdirdata = negdirdata.astype(float)
negdirdata = negdirdata[::-1]
print(negdirdata)

##positive directional indicator for VIXY
posdiurl = 'https://www.alphavantage.co/query?function=PLUS_DI&symbol=VIXY&interval=daily&time_period='+str(return_horizon)+'&apikey=' + key
posdirdata = pd.DataFrame(requests.get(posdiurl).json()["Technical Analysis: PLUS_DI"]).transpose()
posdirdata.index = pd.to_datetime(posdirdata.index)
posdirdata = posdirdata.astype(float)
posdirdata = posdirdata[::-1]
print(posdirdata)

##positive DMI indicator for VIXY
posdmiurl = 'https://www.alphavantage.co/query?function=PLUS_DM&symbol=VIXY&interval=daily&time_period='+str(return_horizon)+'&apikey=' + key
posdmidata = pd.DataFrame(requests.get(posdmiurl).json()["Technical Analysis: PLUS_DM"]).transpose()
posdmidata.index = pd.to_datetime(posdmidata.index)
posdmidata = posdmidata.astype(float)
posdmidata = posdmidata[::-1]
print(posdmidata)

##positive DMI indicator for VIXY
negdmiurl = 'https://www.alphavantage.co/query?function=MINUS_DM&symbol=VIXY&interval=daily&time_period='+str(return_horizon)+'&apikey=' + key
negdmidata = pd.DataFrame(requests.get(negdmiurl).json()["Technical Analysis: MINUS_DM"]).transpose()
negdmidata.index = pd.to_datetime(negdmidata.index)
negdmidata = negdmidata.astype(float)
negdmidata = negdmidata[::-1]
print(negdmidata)

##colormap visualization(QQQ)
import matplotlib.pyplot as plt

##set X values (n-day vix return till T-1 at close)
X = (vix_price['5. adjusted close'].shift(1)/vix_price['5. adjusted close'].shift(1+return_horizon))-1

##set Y values (n-day change in negative directional indicator)
Y = (negdirdata.shift(1)/negdirdata.shift(1+return_horizon))-1

##set return datapoints (remove outliers)
spy_return = spy_price['5. adjusted close'].pct_change(periods=-return_horizon)
low_boundary = spy_return.mean() - spy_return.std() * 2 ##2 times std
print(low_boundary)
high_boundary = spy_return.mean() + spy_return.std() * 2
print(high_boundary)
spy_return = spy_return[np.logical_and((spy_return > low_boundary),(spy_return < high_boundary))]

spy_return = spy_return[spy_return < 0]

##combine by inner join
test_set = pd.concat([X,Y,spy_return], axis=1, join='inner', ignore_index=False)

#test_set = X.join(Y, how="inner", left_index=True, right_index=True).join(qqq_price['5. adjusted close'].pct_change(periods=-1), how="inner", left_index=True, right_index=True)
test_set.columns = ['VIX_change', 'VIX_Negative_DI', 'spy_return']

test_set.plot(kind="scatter", 
              x='VIX_change', 
              y='VIX_Negative_DI',
              alpha=0.4,
              s = abs(test_set['spy_return'])*1000,
              label="return visualization spy", 
              figsize=(12,10),
              c = 'spy_return',
              cmap=plt.get_cmap("Blues"), 
              colorbar=True,
              xlim = (-1.0, 1.0),
              ylim = (-1.0, 1.0)
)

##colormap visualization(QQQ)
import matplotlib.pyplot as plt

##set X values (standard scaled) (n-day vix return till T-1 at close)
X = np.log(posdmidata.shift(1))
#X = (posdmidata.shift(1) - posdmidata.shift(1).mean())/posdmidata.shift(1).std()

##set Y values (n-day change in negative directional indicator)
Y = np.log(negdmidata.shift(1))
#Y = (negdmidata.shift(1) - negdmidata.shift(1).mean())/negdmidata.shift(1).std()

##set return datapoints (remove outliers)
spy_return = spy_price['5. adjusted close'].pct_change(periods=-return_horizon)
low_boundary = spy_return.mean() - spy_return.std() * 1 ##2 times std
print(low_boundary)
high_boundary = spy_return.mean() + spy_return.std() * 1
print(high_boundary)
spy_return = spy_return[np.logical_and((spy_return > low_boundary),(spy_return < high_boundary))]

spy_return = spy_return[spy_return < 0]

##combine by inner join
test_set = pd.concat([X,Y,spy_return], axis=1, join='inner', ignore_index=False)

#test_set = X.join(Y, how="inner", left_index=True, right_index=True).join(qqq_price['5. adjusted close'].pct_change(periods=-1), how="inner", left_index=True, right_index=True)
test_set.columns = ['VIX_Positive_DM', 'VIX_Negative_DM', 'spy_return']

test_set.plot(kind="scatter", 
              x='VIX_Positive_DM', 
              y='VIX_Negative_DM',
              alpha=0.4,
              s = abs(test_set['spy_return'])*1000,
              label="return visualization spy", 
              figsize=(12,10),
              c = 'spy_return',
              cmap=plt.get_cmap("Blues"), 
              colorbar=True,
              #xlim = (-1.0, 1.0),
              #ylim = (-1.0, 1.0)
)

##double dmi
import matplotlib.pyplot as plt

##set X values (n-day vix return till T-1 at close)
X = (posdirdata.shift(1)/posdirdata.shift(1+return_horizon))-1

##set Y values (n-day change in negative directional indicator)
Y = (negdirdata.shift(1)/negdirdata.shift(1+return_horizon))-1

##set return datapoints (remove outliers)
spy_return = spy_price['5. adjusted close'].pct_change(periods=-return_horizon)
low_boundary = spy_return.mean() - spy_return.std() * 2 ##2 times std
print(low_boundary)
high_boundary = spy_return.mean() + spy_return.std() * 2
print(high_boundary)
spy_return = spy_return[np.logical_and((spy_return > low_boundary),(spy_return < high_boundary))]

spy_return = spy_return[spy_return > 0]

##combine by inner join
test_set = pd.concat([X,Y,spy_return], axis=1, join='inner', ignore_index=False)

#test_set = X.join(Y, how="inner", left_index=True, right_index=True).join(qqq_price['5. adjusted close'].pct_change(periods=-1), how="inner", left_index=True, right_index=True)
test_set.columns = ['VIX_Positive_DI', 'VIX_Negative_DI', 'spy_return']

test_set.plot(kind="scatter", 
              x='VIX_Positive_DMI', 
              y='VIX_Negative_DMI',
              alpha=0.4,
              s = abs(test_set['spy_return'])*1000,
              label="return visualization spy", 
              figsize=(12,10),
              c = 'spy_return',
              cmap=plt.get_cmap("Reds"), 
              colorbar=True,
              xlim = (-1.0, 1.0),
              ylim = (-1.0, 1.0)
)

