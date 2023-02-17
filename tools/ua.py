import random

from tools.config import MyMysql


class UaPool:
    def __init__(self):
        database = MyMysql()
        db = database.connect
        cur = database.cursor

        sql = 'select useragent from ua_pool where types = %s and popularity != %s'
        cur.execute(sql, ('Windows', 'Uncommon'))
        data_d = cur.fetchall()
        desktop_list = []
        for data_d_per in data_d:
            desktop_list.append(data_d_per[0])
        self.desktop = desktop_list

        cur.execute(sql, ('Android', 'Uncommon'))
        data_m = cur.fetchall()
        mobile_list = []
        for data_m_per in data_m:
            mobile_list.append(data_m_per[0])
        self.mobile = mobile_list

        cur.close()
        db.close()

    def choose_ua(self, platform='desktop'):
        if platform == 'desktop':
            return random.choice(self.desktop)
        elif platform == 'mobile':
            return random.choice(self.mobile)
        else:
            return random.choice(self.desktop)



if __name__ == '__main__':
    up = UaPool()
    print(up.choose_ua())