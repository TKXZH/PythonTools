#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import requests
from bs4 import BeautifulSoup
import csv

begin = datetime.date(2013,10,31)
end = datetime.date(2019,12,1)
d = begin

delta = datetime.timedelta(days=1)
while d <= end:
    current = d.strftime("%Y-%m-%d")
    response = requests.get('http://q-weather.info/weather/54511/history/?date=' + current)
    html = BeautifulSoup(response.text)
    try:
        table = html.body.table.tbody
    except AttributeError:
        d += delta
        continue
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)

    print(output_rows)
    with open('output.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)
    d += delta


