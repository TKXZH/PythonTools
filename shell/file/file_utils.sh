#!/usr/bin/env bash

# 合并某些文件夹下的某些文件
# e.g: find -exec command {} \;
find . -type f -name xxx.csv -exec cat {} \;>all_files.txt