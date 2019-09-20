#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser

df_ferrara = pd.read_csv('data/ferrara_270615.csv')
df_milano = pd.read_csv('data/milano_270615.csv')
df_mantova = pd.read_csv('data/mantova_270615.csv')
df_ravenna = pd.read_csv('data/ravenna_270615.csv')
df_torino = pd.read_csv('data/torino_270615.csv')
df_faenza = pd.read_csv('data/faenza_270615.csv')
df_asti = pd.read_csv('data/asti_270615.csv')
df_bologna = pd.read_csv('data/bologna_270615.csv')
df_piacenza = pd.read_csv('data/piacenza_270615.csv')
df_cesena = pd.read_csv('data/cesena_270615.csv')
pd.DataFrame()

y1 = df_ravenna['temp']
x1 = df_ravenna['day']
y2 = df_faenza['temp']
x2 = df_faenza['day']
y3 = df_cesena['temp']
x3 = df_cesena['day']
y4 = df_milano['temp']
x4 = df_milano['day']
y5 = df_asti['temp']
x5 = df_asti['day']
y6 = df_torino['temp']
x6 = df_torino['day']

fig, ax = plt.subplots()

dist = [df_ravenna['dist'][0],
    df_cesena['dist'][0],
    df_faenza['dist'][0],
    df_ferrara['dist'][0],
    df_bologna['dist'][0],
    df_mantova['dist'][0],
    df_piacenza['dist'][0],
    df_milano['dist'][0],
    df_asti['dist'][0],
    df_torino['dist'][0]
]

# temp_max 是一个存放每个城市最高温度的列表
temp_max = [df_ravenna['temp'].max(),
    df_cesena['temp'].max(),
    df_faenza['temp'].max(),
    df_ferrara['temp'].max(),
    df_bologna['temp'].max(),
    df_mantova['temp'].max(),
    df_piacenza['temp'].max(),
    df_milano['temp'].max(),
    df_asti['temp'].max(),
    df_torino['temp'].max()
]

# temp_min 是一个存放每个城市最低温度的列表
temp_min = [df_ravenna['temp'].min(),
    df_cesena['temp'].min(),
    df_faenza['temp'].min(),
    df_ferrara['temp'].min(),
    df_bologna['temp'].min(),
    df_mantova['temp'].min(),
    df_piacenza['temp'].min(),
    df_milano['temp'].min(),
    df_asti['temp'].min(),
    df_torino['temp'].min()
 ]

dist1 = dist[0:5]
dist2 = dist[5:10]
# dist1 = [[x] for x in dist1]
# dist2 = [[x] for x in dist2]
dist1 = np.array(dist1).reshape(5, 1)
dist2 = np.array(dist2).reshape(5, 1)


temp_max1 = temp_max[0:5]
temp_max2 = temp_max[5:10]


from sklearn.svm import SVR
svr_lin1 = SVR(kernel='linear', C=1e3)
svr_lin2 = SVR(kernel='linear', C=1e3)

svr_lin1.fit(dist1, temp_max1)
svr_lin2.fit(dist2, temp_max2)

xp1 = np.arange(10,100,10).reshape((9,1))
xp2 = np.arange(50,400,50).reshape((7,1))

yp1 = svr_lin1.predict(xp1)
yp2 = svr_lin2.predict(xp2)

ax.plot(xp1, yp1, 'r', xp2, yp2, 'b', dist, temp_max, 'go')
plt.show()
