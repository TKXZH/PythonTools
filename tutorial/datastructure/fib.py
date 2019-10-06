#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zonghuixu'


def fib(max):
    a, b = 0, 1
    while a < max:
        print(a)
        a, b = b, (a+b)

def fib_gen(max):
    a, b = 0, 1
    while a < max:
        yield a
        a, b = b, (a+b)

fib_generator = fib_gen(15)
for item in fib_generator:
    print(item)

