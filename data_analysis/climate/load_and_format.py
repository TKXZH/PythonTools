#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

climate = pd.read_csv('data/climate.csv', index_col=u'时间', encoding='GBK')
# rename column names
climate.rename(columns={u'风速': 'wind', u'压强': 'pressure', u'降水量': 'rain', u'温度': 'temperature', u'湿度': 'humidity'}, inplace=True)
climate.index = pd.to_datetime(climate.index)
climate[['PM2.5', 'PM10']].plot()
plt.show()

