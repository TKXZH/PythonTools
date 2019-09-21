#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import timedelta

data1 = pd.read_excel('data/文件1.xlsx', index_col='时间')
data2 = pd.read_excel('data/文件2.xlsx', index_col='时间')
data3 = pd.read_excel('data/文件3.xlsx', index_col='时间')


def pre(vehicle_df: pd.DataFrame):
    print('处理之前文件的行数为:{}'.format(vehicle_df.shape[0]))
    ## 格式化时间字段
    vehicle_df.index = pd.to_datetime(vehicle_df.index, format='%Y/%m/%d %H:%M:%S.000.')
    vehicle_df['时间'] = vehicle_df.index
    return vehicle_df


# def operation1(vehicle_df: pd.DataFrame) -> pd.DataFrame:
#     # 1. 按秒进行重新采样
#     # 2. 线性回归填充缺失值
#     print("正在进行缺失数据重新采样...")
#     res = vehicle_df.asfreq('1S').interpolate()
#     print('填补缺失数据后的行数为:{}'.format(res.shape[0]))
#     return res

def operation1(vehicle_df: pd.DataFrame) -> pd.DataFrame:
    # 1. 按秒进行重新采样
    # 2. 只重新填充一秒以内的缺失数据
    print("正在进行缺失数据重新采样...")
    res = vehicle_df.asfreq('1S').fillna(method='bfill',limit=1).dropna()
    print('填补缺失数据后的行数为:{}'.format(res.shape[0]))
    return res



def operation2(vehicle_df: pd.DataFrame) -> pd.DataFrame:
    return vehicle_df

def operation3(vehicle_df: pd.DataFrame) -> pd.DataFrame:
    last_x, last_y = 0, 0
    last_time = None
    tobe_removed = set()
    current_set = set()
    park_start_time = None
    over_time = False

    # 遍历每一行
    for _, row in vehicle_df.iterrows():
        # 检测到和上一记录于相同位置
        if last_x==row.纬度 and last_y==row.经度:

            current_set.add(row.name)

            # 刚开始停车
            if park_start_time is None:
                park_start_time = last_time
            else:
                # 停车超过一分钟
                if park_start_time + timedelta(seconds=60) < row.name:
                    over_time = True
        # 结束停车
        else:
            park_start_time = None
            if over_time:
                print("检测到长时间停车...")
                print(sorted(current_set))
                tobe_removed = tobe_removed | current_set
            current_set = set()
            over_time = False

        last_x = row.纬度
        last_y = row.经度
        last_time = row.name
    res = vehicle_df[~vehicle_df.index.isin(tobe_removed)]
    print('Operation3后的行数为:{}'.format(res.shape[0]))
    return res


def operation4(vehicle_df: pd.DataFrame) -> pd.DataFrame:
    low_speed_start_time = None
    current_set = set()
    tobe_removed = set()
    low_speed_over_time = False
    for _, row in vehicle_df.iterrows():
        if row.GPS车速 < 10:
            current_set.add(row.name)
            if low_speed_start_time is None:
                low_speed_start_time = row.name
            else:
                if low_speed_start_time + timedelta(seconds=180) < row.name:
                    low_speed_over_time = True
        else:
            if low_speed_over_time:
                print("检测到长时间低速...")
                print(sorted(current_set))
                tobe_removed = tobe_removed | current_set
            low_speed_over_time = False
            low_speed_start_time = None
            current_set = set()
    res = vehicle_df[~vehicle_df.index.isin(tobe_removed)]
    print('Operation4后的行数为:{}'.format(res.shape[0]))
    return res

def clean(data, name):
    formatted = pre(data)
    after_process1 = operation1(formatted)
    after_process2 = operation2(after_process1)
    after_process3 = operation3(after_process2)
    after_process4 = operation4(after_process3)
    after_process4.to_csv(name + '.csv',index=None)

if __name__ == '__main__':
    clean(data1, '文件1')
    clean(data2, '文件2')
    clean(data3, '文件3')

