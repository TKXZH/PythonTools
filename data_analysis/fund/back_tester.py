# -*- coding: utf-8 -*-
# !/usr/bin/env python

from __future__ import division

import pandas as pd

import spider


class BackTester:
    def __init__(self, strategy, his_data):
        self.shares = 0
        self.stock = 0
        self.strategy = strategy
        self.his_data = his_data

    def roll(self):
        length = len(self.his_data)
        for day in range(length):
            active_date = self.his_data[length - day - 1:length]
            current_date_data = active_date.iloc[0]
            nums = self.strategy(active_date)
            print(current_date_data['净值日期'] + '买入' + str(nums))
            self.shares += nums
            self.stock += nums * float(current_date_data['单位净值'])
        last_value = self.shares * float(self.his_data.loc[0, '单位净值'])
        profit = (last_value - self.stock) / self.stock
        print("回测结束，盈利率 " + str(profit))
        print("总盈利" + str(last_value - self.stock))


def regular(his_data_frame):
    return 1000


a = BackTester(regular, pd.DataFrame(spider.fetch_from_east_money('2019-04-06', '2019-08-09', '000962')))
a.roll()
