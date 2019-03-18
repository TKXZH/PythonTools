#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'


class BinarySortTree:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def put(self, value):
        if self.value >= value:
            if self.left is None:
                self.left = BinarySortTree(value, None, None)
            else:
                self.left.put(value)
        else:
            if self.right is None:
                self.right = BinarySortTree(value, None, None)
            else:
                self.right.put(value)

    def find(self, value):
        if self.value == value:
            print("got the value!")
            return
        if value <= self.value:
            if self.left is not None:
                self.left.find(value)
            else:
                print("can not find")
        if value > self.value:
            if self.right is not None:
                self.right.find(value)
            else:
                print("can not find")


def test():
    bst = BinarySortTree(50, None, None)
    for i in range(1, 100):
        bst.put(i)
    bst.find(22)


test()

