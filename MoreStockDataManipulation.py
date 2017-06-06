#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 17:50:30 2017

@author: Abhishek1Mahesh
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web


style.use('ggplot')

#df = data frame

df = pd.read_csv('tsla.csv', parse_dates= True, index_col = 0)

#creating a moving average column of 100 days--> when 50ma crosses above the 100ma, that signals an uptrend in price

#df['100ma'] = df['Adj Close'].rolling(window=100, min_periods = 0).mean()

#the parameters for subplot2grid(size, location, amount of rows, amount of cols, joins itself to the previous plot)

#resampling data--------- OHLC- Open High Low Close


df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').ohlc()

print(df_ohlc.head())

df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)


ax1 = plt.subplot2grid((6,1),(0,0), rowspan= 5, colspan = 1)
ax2 = plt.subplot2grid((6,1),(5,0), rowspan= 1, colspan = 1, sharex=ax1)
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
#ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)

plt.show()