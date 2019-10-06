#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import os
print('process (%s) starts...' % os.getpid())

pid = os.fork()
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

from multiprocessing import Process
