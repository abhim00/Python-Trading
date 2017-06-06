#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 17:30:38 2017

@author: Abhishek1Mahesh
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web


style.use('ggplot')

#df = data frame

df = pd.read_csv('tsla.csv', parse_dates= True, index_col = 0)

#creating a moving average column of 100 days--> when 50ma crosses above the 100ma, that signals an uptrend in price

df['100ma'] = df['Adj Close'].rolling(window=100, min_periods = 0).mean()

df.dropna(inplace=True)
#df.fillna(value= 0, inplace = True)
print(df.tail())

#the parameters for subplot2grid(size, location, amount of rows, amount of cols, joins itself to the previous plot)

ax1 = plt.subplot2grid((6,1),(0,0), rowspan= 5, colspan = 1)
ax2 = plt.subplot2grid((6,1),(5,0), rowspan= 1, colspan = 1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])