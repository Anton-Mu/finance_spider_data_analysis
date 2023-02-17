import random
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import requests
from bs4 import BeautifulSoup

from tools.config import MyMysql
from tools.ua import UaPool


def eastmoney_guba_spider(code, time_frame):
    database = MyMysql()
    db = database.connect
    cur = database.cursor
    ua_p = UaPool()

    flag = True
    data_list = []

    # 转换股票代码为东财股吧识别格式
    if code == 'sh000001':
        code = 'zssh000001'
    elif 'sh' in code:
        code = code.replace('sh', '')
    # 存储上一条日期，以经过对比发现年份变化
    last_date_time = None
    for page in range(300):
        if flag:
            page += 1
            url = "http://guba.eastmoney.com/list," + str(code) + "_" + str(page) + ".html"
            ua = ua_p.choose_ua()
            headers = {
                'User-Agent': ua
            }
            try:
                res = requests.get(url, headers=headers, timeout=10).text
            except:
                continue
            bs = BeautifulSoup(res, 'html.parser')
            for div in bs.select('div .normal_post'):
                view_num = div.select('.l1')[0].string
                comment_num = div.select('.l2')[0].string
                try:
                    content = div.select('.l3')[0].a['title']
                except KeyError:
                    content = div.select('.l3')[0].select('a')[1]['title']
                author = div.select('.l4')[0].a.font.string
                date_time = parse(div.select('.l5')[0].string)
                print(view_num, comment_num, content, author, date_time)
                if not last_date_time:
                    last_date_time = date_time
                # 若较早发的帖子日期经过格式化后日期晚于较晚发的帖子，则认为年份发生变化
                if last_date_time < date_time:
                    date_time = date_time - relativedelta(years=1)
                if (datetime.now() - date_time).days > time_frame:
                    flag = False
                # sql = 'insert ignore into eastmoney_guba ' \
                #       '(code, content, author, datetime, view_num, comment_num) ' \
                #       'VALUES (%s, %s, %s, %s, %s, %s)'
                # cur.execute(sql, (code, content, author, date_time, view_num, comment_num))
                # db.commit()
                data_list.append((code, content, author, date_time, view_num, comment_num))
            if len(data_list) > 500:
                sql = 'insert ignore into eastmoney_guba ' \
                      '(code, content, author, datetime, view_num, comment_num) ' \
                      'VALUES (%s, %s, %s, %s, %s, %s)'
                cur.executemany(sql, data_list)
                db.commit()
                data_list = []
                print("500条批量存储完成。")
        else:
            break
        time.sleep(random.randint(5, 10))

    print(datetime.now())
    sql = 'insert ignore into eastmoney_guba ' \
          '(code, content, author, datetime, view_num, comment_num) ' \
          'VALUES (%s, %s, %s, %s, %s, %s)'
    cur.executemany(sql, data_list)
    db.commit()
    print(datetime.now())
    print("全部存储完成。")
    cur.close()
    db.close()


if __name__ == "__main__":
    eastmoney_guba_spider('sh688180', 3)
