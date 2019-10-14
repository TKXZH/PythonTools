#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = 'zonghuixu'

import demjson
import re
import requests
from bs4 import BeautifulSoup
from . import config



def fetch_from_east_money_by_page(date_start, date_end, code, page):
    response = requests.get(config.fund_detail_url,
                            {'code': code,
                             'sdate': date_start,
                             'edate': date_end,
                             'page': page})

    match_res = re.match('^.*?({.*}).*$', response.text)

    json_str = match_res.group(1)
    fund_data = demjson.decode(json_str)
    html = BeautifulSoup(fund_data['content'])
    headers = html.table.thead.tr.find_all('th')
    headers = map(lambda x: x.text.encode('utf-8'), headers)

    prettified_date = []
    for tr in html.table.tbody:
        row = tr.find_all('td')
        row = map(lambda x: x.text.encode('utf-8'), row)
        prettified_date.append(dict(zip(headers, row)))

    return prettified_date


def fetch_from_east_money(date_start, date_end, code):
    response = requests.get(config.fund_detail_url,
                            {'code': code,
                             'sdate': date_start,
                             'edate': date_end})

    match_res = re.match('^.*?({.*}).*$', response.text)

    data = []
    json_str = match_res.group(1)
    fund_data = demjson.decode(json_str)
    for page in range(1, fund_data['pages']+1):
        data += fetch_from_east_money_by_page(date_start, date_end, code, page)

    return data


# print pd.DataFrame(fetch_from_east_money('2017-12-12', '2019-09-11', 377240))
