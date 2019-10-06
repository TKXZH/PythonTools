#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import pandas as pd


def select(df, columns):
    if type(columns) != list:
        raise Exception('columns should be list!')
    return df[columns]

roq = pd.read_csv("/Users/zonghuixu/Downloads/roq_result.csv")

print(roq[roq.sku == 134359]['forecast21Avg'])

