#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import seaborn as sns
import pandas as pd
planets: pd.DataFrame = sns.load_dataset('planets')
print(planets)
print(planets .pivot_table(index='method', columns='mass'))