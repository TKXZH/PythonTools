#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import pandas as pd


def select(df, columns):
    if type(columns) != list:
        raise Exception('columns should be list!')
    return df[columns]


pd.DataFrame.select = select
