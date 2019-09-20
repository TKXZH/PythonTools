#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

# 装饰器
# 执行带有装饰器的方法时，首先将被调用方法传入装饰器，执行装饰器方法，然后将当前方法的参数传入装饰器返回的方法中并进行调用
# 相当于执行now = log(now)


def log(fun):
    def wrapper(*args, **kwargs):
        print('enhanced!')
        return fun(*args, **kwargs)
    return wrapper


# 相当于执行now = better_log(prefix)(now)
def better_log(prefix):
    def log(fun):
        def wrapper(*args, **kwargs):
            print(prefix + 'enhanced!')
            return fun(*args, **kwargs)
        return wrapper
    return log


@better_log('[test]')
def hello():
    print('hello!')


hello()





