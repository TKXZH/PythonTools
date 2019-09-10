#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import basic_csv_parser
import matplotlib.pyplot as plt
csv = basic_csv_parser.get_data_frame("roq_output_simple.csv")

# filter columns to new data frame
sku_band = csv[['sku', 'band']]

# filter by condition
band = csv[csv['band'] == 'A']
band = csv[csv.band == 'A']
# filter by multiple conditions (and "in" logic in SQL)
sku_set = [10071986, 84709, 1828948, 1828950]
band_and_sku = csv[(csv['band'] == 'A') & csv['sku'].isin(sku_set)].copy()

# update data
band_and_sku.loc[372, 'sku'] = 3

# add column
# An indexer that gets on a single-dtyped object is almost always a view
band_and_sku['price'] = band_and_sku['band'] + '+_+'
band_and_sku.loc[band_and_sku.band == 'A', 'band'] = 'B'

# group by and sum
sum_res = csv.groupby(['band'])['logicRoqResult'].sum().reset_index()
print(sum_res)

# group by and count
value_counts = csv['band'].value_counts()


# apply function
def supply(series):
    print(series)


# axis 0: columns 1: rows
csv.apply(supply, 0)
csv.read('roq_output.csv')


