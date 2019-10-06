#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import pandas as pd
import numpy as np
from scipy.interpolate import lagrange

data = pd.DataFrame(np.random.rand(30).reshape([10, 3]))
data.loc[1, 2] = None
data.loc[2, 2] = None
data.loc[3, 2] = None
data.loc[4, 2] = None

print(data)
data_count = data.count()
na_count = len(data) - data_count
na_rate = na_count / len(data)
result = pd.concat([data_count, na_count, na_rate], axis=1)

def ployinterp_column(s,n,k=5):
    y = s[list(range(n-k,n)) + list(range(n+1,n+1+k))]
    y = y[y.notnull()]
    return lagrange(y.index,list(y))(n)


data = data[~data[2].isnull() | ~data[2].shift().isnull()]

for i in data.columns:
    for j in range(len(data)):
        if (data[i].isnull()).iloc[j]:
            data[i][j] = ployinterp_column(data[i],j)

from datetime import timedelta
t = timedelta(0)
# data.index = [list('abcdefg')]
# print(data[1][1])
# print(data)


class Game:
    def __init__(self, age):
        self.age = age

    def __str__(self):
        return "fixed"

res = data.apply(lambda x: x.apply(lambda y:Game(y)))
print(res[0].dtype)

