import re
import time
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime

from tools.config import MyMysql
from tools.ua import UaPool


def sina_finance_spider(code, time_frame):
    datebase = MyMysql()
    db = datebase.connect
    cur = datebase.cursor
    ua_p = UaPool()

    flag = True
    data_list = []
    for page in range(300):
        if flag:
            page += 1
            url = "https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=" + code + "&Page=" + str(page)
            ua = ua_p.choose_ua()
            headers = {
                'user-agent': ua
            }
            res = requests.get(url, headers=headers).text
            bs = BeautifulSoup(res, 'html.parser')
            count = 0
            date_time_list = []
            content_list = []
            for child in bs.select('div .datelist')[0].ul.children:
                # 过滤<br>标签
                if child.string and re.sub(r"\s+", "", child.string):
                    try:
                        if count == 0:
                            date_time_list.append(parse(child.string))
                            count = 1
                        elif count == 1:
                            content_list.append(re.sub(r"\s+", "", child.string))
                            count = 0
                    except Exception as e:
                        continue
            for i in range(len(date_time_list)):
                date_time = date_time_list.pop()
                content = content_list.pop()
                if (datetime.now() - date_time).days > time_frame:
                    flag = False
                # sql = 'insert ignore into sina_finance (code, content, datetime) ' \
                #       'VALUES (%s, %s, %s)'
                # cur.execute(sql, (code, content, date_time))
                # db.commit()
                data_list.append((code, content, date_time))
                print(date_time)
                print(content)
            time.sleep(5)

    print(datetime.now())
    sql = 'insert ignore into sina_finance (code, content, datetime) ' \
          'VALUES (%s, %s, %s)'
    cur.executemany(sql, data_list)
    db.commit()
    print(datetime.now())
    print("全部批量存储完成。")
    cur.close()
    db.close()


if __name__ == '__main__':
    sina_finance_spider('sh688180', 3)
