import pandas as pd

import datetime

today = datetime.date.today()
for i in range(1, 370):
    today = today + datetime.timedelta(days=1)
    if today.weekday()== 5 or today.weekday() == 6:
        print(today.strftime('%Y%m%d' ))
