#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

import pandas as pd
from scipy.interpolate import lagrange

data1 = pd.read_excel('data/文件1.xlsx', index_col='时间')
data2 = pd.read_excel('data/文件2.xlsx', index_col='时间')
data3 = pd.read_excel('data/文件3.xlsx', index_col='时间')


def ployinterp_column(s, n, k=2):
    s.index = [x for x in range(len(s.index))]
    y = s[list(range(n - k, n)) + list(range(n + 1, n + 1 + k))]
    y = y[y.notnull()]
    return lagrange(y.index, list(y))(n)


def pre(vehicle_df: pd.DataFrame):
    print('处理之前文件的行数为:{}'.format(vehicle_df.shape[0]))
    ## 格式化时间字段
    vehicle_df.index = pd.to_datetime(vehicle_df.index, format='%Y/%m/%d %H:%M:%S.000.')
    return vehicle_df


# def operation1(vehicle_df: pd.DataFrame) -> pd.DataFrame:
#     # 1. 按秒进行重新采样
#     # 2. 线性回归填充缺失值
#     print("正在进行缺失数据重新采样...")
#     res = vehicle_df.asfreq('1S').interpolate()
#     print('填补缺失数据后的行数为:{}'.format(res.shape[0]))
#     return res

# def operation1(vehicle_df: pd.DataFrame) -> pd.DataFrame:
#     # 1. 按秒进行重新采样
#     # 2. 只重新填充一秒以内的缺失数据
#     print("正在进行缺失数据重新采样...")
#     res = vehicle_df.asfreq('1S').fillna(method='bfill',limit=1).dropna()
#     print('填补缺失数据后的行数为:{}'.format(res.shape[0]))
#     return res

def operation1(vehicle_df: pd.DataFrame) -> pd.DataFrame:
    # 1. 按秒进行重新采样
    print("正在进行缺失数据重新采样...")
    res = vehicle_df.asfreq('1S')

    # 2. 限制缺失数据在一秒以内才填充
    res = res[~res.加速度.isnull() | ~res.加速度.shift().isnull()]

    print("正在进行拉格朗日插值...")
    # 3. 拉格朗日插值
    for i in res.columns:
        for j in range(len(res)):
            if (res[i].isnull()).iloc[j]:
                res[i][j] = ployinterp_column(res[i], j)

    res['时间'] = res.index
    print('填补缺失数据后的行数为:{}'.format(res.shape[0]))
    return res


# 老版本加速度算法
# def operation2(vehicle_df: pd.DataFrame) -> pd.DataFrame:
#     last_speed = None
#     last_time = None
#     tobe_removed = set()
#     for _, row in vehicle_df.iterrows():
#         if last_time is not None and last_speed is not None and (last_time + timedelta(seconds=1)) == row.时间:
#             a = row.GPS车速 - last_speed
#             if a > 3.968 or a < -8:
#                 print("检测到加速度异常:{}".format(a))
#                 tobe_removed.add(row.name)
#         last_speed = row.GPS车速
#         last_time = row.时间
#     res = vehicle_df[~vehicle_df.index.isin(tobe_removed)]
#     print('Operation2后的行数为:{}'.format(res.shape[0]))
#     return res


# 直接用新列作为加速度
def operation2(vehicle_df: pd.DataFrame) -> pd.DataFrame:
    res = vehicle_df[(vehicle_df.加速度 < 3.988) & (vehicle_df.加速度 > -8)]
    print('Operation2后的行数为:{}'.format(res.shape[0]))
    return res


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
        if last_x == row.纬度 and last_y == row.经度:

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
    after_process4.to_csv(name + '.csv', index=None)
    split_file_by_speed_round(after_process4, name)


def split_file_by_speed_round(vehicle_df: pd.DataFrame, name: str):
    selected_index_list = []
    selected_index = set()
    last_is_zero = True
    for _, row in vehicle_df.iterrows():
        if row.GPS车速 == 0:
            if last_is_zero:
                selected_index.add(row.name)
            else:
                if len(selected_index) > 10:
                    selected_index_list.append(selected_index)
                    selected_index = {row.name}
            last_is_zero = True
        else:
            selected_index.add(row.name)
            last_is_zero = False
    features = []
    for i, index_set in enumerate(map(lambda x: sorted(x), selected_index_list)):
        single_part = vehicle_df.loc[index_set]
        feature = analysis_feature(single_part, name, i)
        if feature['运行里程'] > 0 and feature['平均速读'] > 0 and feature['加速段平均加速度'] != 0 and feature['减速段平均减速度'] != 0:
            single_part.to_csv('{}_part_{}.csv'.format(name, i), index=None)
            features.append(feature)

    columns = ['序号', '运行时间', '加速时间', '减速时间', '匀速时间', '怠速时间', '运行里程', '最大速度', '最大加速度', '最大减速度', '平均速读', '运行平均速读',
               '加速段平均加速度', '减速段平均减速度', '速度标准差', '加速度标准差']
    pd.DataFrame(features).reindex(columns=columns).to_csv("features_{}.csv".format(name), index=None)


def analysis_feature(vehicle_df: pd.DataFrame, name: str, index: int):
    analysis_result = dict()
    analysis_result['序号'] = name + '_' + str(index)

    # 1. 运行时间
    total_time = vehicle_df.iloc[-1].name - vehicle_df.iloc[0].name
    analysis_result['运行时间'] = total_time.seconds

    # 2. 加速时间
    # 3. 减速时间
    # 5. 怠速时间
    accelerate_time = timedelta(0)
    decelerate_time = timedelta(0)
    idling_time = timedelta(0)
    last_time = None
    time_gap = None
    acc_speed_sum = 0
    dec_speed_sum = 0
    for _, row in vehicle_df.iterrows():
        if last_time is not None:
            time_gap = row.name - last_time
        if time_gap is not None:
            if row.加速度 > 0.1:
                accelerate_time = accelerate_time + time_gap
                acc_speed_sum += row.加速度
            if row.加速度 < -0.1:
                decelerate_time = decelerate_time + time_gap
                dec_speed_sum += row.加速度
            if row.GPS车速 == 0:
                idling_time = decelerate_time + time_gap
        last_time = row.name
    analysis_result['加速时间'] = accelerate_time.seconds
    analysis_result['减速时间'] = decelerate_time.seconds
    analysis_result['怠速时间'] = idling_time.seconds

    # 4. 匀速时间
    analysis_result['匀速时间'] = (total_time - decelerate_time - accelerate_time - idling_time).seconds

    # 6. 运行里程
    S = vehicle_df.GPS车速.sum() / 3600
    analysis_result['运行里程'] = S

    # 7. 最大速度
    analysis_result['最大速度'] = vehicle_df.GPS车速.max()
    # 8. 最大加速度
    analysis_result['最大加速度'] = vehicle_df.加速度.max()
    # 9. 最大减速度
    analysis_result['最大减速度'] = vehicle_df.加速度.min()
    # 10. 平均速读
    analysis_result['平均速读'] = S / total_time.seconds
    # 11、运行平均速度
    analysis_result['运行平均速读'] = S / (total_time - idling_time).seconds

    # 12. 加速段平均加速度
    if accelerate_time.seconds == 0:
        analysis_result['加速段平均加速度'] = 0
    else:
        analysis_result['加速段平均加速度'] = acc_speed_sum / accelerate_time.seconds
    # 13. 减速段平均加速度
    if decelerate_time.seconds == 0:
        analysis_result['减速段平均减速度'] = 0
    else:
        analysis_result['减速段平均减速度'] = dec_speed_sum / decelerate_time.seconds
    # 14. 速度标准差
    analysis_result['速度标准差'] = vehicle_df.GPS车速.std()
    # 15. 加速度标准差
    analysis_result['加速度标准差'] = vehicle_df.加速度.std()

    return analysis_result


if __name__ == '__main__':
    clean(data1, '文件1')
    clean(data2, '文件2')
    clean(data3, '文件3')
