import pandas as pd
import os
import csv
from functools import reduce

# 1。读取所有采集下来的关于本地化的招聘文件
def read_files():
    path = './'
    return list(map(lambda p: path + p, os.listdir(path)))

# 2。 将文件合并为一个大文件，便于程序分析
lines = []
for f in read_files():
    csv_file = csv.reader(open(f, 'r'))
    next(csv_file, None)
    for user in csv_file:
        lines.append(reduce(lambda x, y: x + y, user))

# 3。 根据关键字将文件进行过滤，为下一步分析做数据清洗
after_filter_lines = list(filter(lambda line: '本地化' in line and '本地化翻译' in line, lines))
print(len(after_filter_lines))

# 4。 定义数据特征分组关系
standard = {'语言能力': ['听说读写', '口头书面', '口头书面表达', '双语能力', '中外文语言及互译能力'],
            '工作态度': ['态度端正', '工作积极', '积极主动', '热情', '责任心', '耐心', '细心', '细致'],
            '英语等级证书': ['英语四级', '英语六级', '英语专业四级', '英语专业八级'],
            '思维学习能力': ['分析问题', '独立思考', '学习'],
            '团队合作': ['团队协作', '团队精神', '协作精神', '合作意识', '团队运营'],
            '工作经验': ['工作经验不限制', ' 应届毕业生'],
            '计算机': ['翻译技术', '翻译软件', '计算机能力', 'CAT', '计算机辅助翻译软件', 'office', '办公软件', '计算机操作技能', 'trados'],
            '沟通': [' 沟通协调', '表达能力', '维护关系'],
            '抗压': ['心理素质', '抗压能力'],
            '本地化知识': ['游戏本地化', '本地化能力', '本地化技术'],
            '意愿,热爱': ['热爱游戏', '游戏行业'],
            '组织协调': ['管理团队', '解决问题', '妥协', '灵活'],
            '服从,安排': ['领导', '上级'],
            '应变': ['适应能力', '突发事件'],
            '服务意识': [' 服务能力'],
            '身体': ['形象好'],
            '执行力': ['执行力强', '效率高'],
            '性格': ['性格外向', '活泼开朗'],
            '翻译': ['中英翻译', '翻译技能', '翻译知识', 'CATTI', '翻译证书', '文本审校、翻译质量', '质量评估', '翻译过程', '质量控制']}

# 5。 进行数据特征提取
metrics = {}
for line in after_filter_lines:
    for k, v in standard.items():
        for item in v:
            if item in line:
                metrics[k] = 1 if k not in metrics else metrics[k] + 1
                break
print(metrics)
