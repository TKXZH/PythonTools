#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

sample_list = [x for x in range(0, 10)]

list1 = sample_list[:3]
print(list1)

list2 = sample_list[1:3]
print(list2)

list3 = sample_list[:-2]
print(list3)

list4 = sample_list[-3:-2]
print(list4)


def trim(string):
    if len(string) == 0:
        return string
    if string[0] != ' ' and string[1] != ' ':
        return string
    elif string[0] == ' ':
        return trim(string[1:])
    else:
        return trim(string[:-1])


print(trim('  hello!   '))
