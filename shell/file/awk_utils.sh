#!/usr/bin/env bash

#判断csv文件某列是否符合要求,注意awk中变量用双引号表示，查询内容中包含双引号则需要转义
awk -F ',' '{if($5=="\"\"") print $0}' /Users/zonghuixu/Downloads/part-m-00000