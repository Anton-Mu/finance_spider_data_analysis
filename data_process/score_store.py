from datetime import datetime
import numpy as np

from sentiment.dict_analysis import DictAnalysis
from tools.config import MyMysql


def box_mean_smooth(data, box_size):
    smoothed_data = np.zeros(len(data))
    for i in range(len(data)):
        box = data[max(0, i-box_size):min(len(data), i+box_size+1)]
        smoothed_data[i] = np.mean(box)
    return smoothed_data


def cal_comment_score(source):
    database = MyMysql()
    db = database.connect
    cur = database.cursor
    data_list = []

    if source == 'guba':
        DA = DictAnalysis('guba')

        sql = 'select id, view_num, comment_num, content ' \
              'from eastmoney_guba ' \
              'where score is null'
        cur.execute(sql)
        data = cur.fetchall()

        # 使用列表推导式
        view_col = [row[1] for row in data]
        comment_col = [row[2] for row in data]

        s_view_col = box_mean_smooth(view_col, 10)
        s_comment_col = box_mean_smooth(comment_col, 10)

        for i in range(len(data)):
            id = data[i][0]
            score = DA.sentiment_score(data[i][3])
            composite_score = score * (s_view_col / 100 + s_comment_col) / 10
            data_list.append((score, composite_score, id))

        sql = 'update eastmoney_guba ' \
              'set score = %s, composite_score = %s ' \
              'where id = %s'
    else:
        DA = DictAnalysis('news')

        sql = 'select id, content ' \
              'from sina_finance ' \
              'where score is null'
        cur.execute(sql)
        data = cur.fetchall()

        for per in data:
            id = per[0]
            score = DA.sentiment_score(per[1])
            data_list.append((score, id))

        sql = 'update sina_finance ' \
              'set score = %s ' \
              'where id = %s'
    cur.executemany(sql, data_list)
    db.commit()

    cur.close()
    db.close()


if __name__ == '__main__':
    print(datetime.now())
    cal_comment_score('guba')
    cal_comment_score('news')
    print(datetime.now())
