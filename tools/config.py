import pymysql


class MyMysql:
    def __init__(self):
        self.connect = pymysql.connect(
            host=Mysql服务IP地址,
            port=Mysql数据库端口,
            user=数据库用户名,
            password=数据库密码,
            database=数据库名,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

