#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import pandas
from os import listdir
from os.path import isfile, join

BASE_DIRS = ['/Users/zonghuixu/Desktop', '/Users/zonghuixu/Downloads', '/Users/zonghuixu/Documents']


def get_data_frame(filename, specific_path=None):
    if specific_path:
        file_path = join(specific_path, filename)
    else:
        target_files = []
        for directory in BASE_DIRS:
            files = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f)) and f == filename]
            target_files += files
        length = len(target_files)

        if length > 1:
            raise Exception("too many files found!", filename)
        elif length == 0:
            raise Exception("0 file found!", filename)
            print("OK")
        else:
            file_path = target_files[0]
    return pandas.read_csv(file_path)
