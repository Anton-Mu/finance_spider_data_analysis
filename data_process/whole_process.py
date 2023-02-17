import time

from data_process.report_generate import generate_report
from data_process.score_store import cal_comment_score
from spider.eastmoney_guba import eastmoney_guba_spider
from spider.sina_finance import sina_finance_spider
from datetime import datetime


def process_data(code):
    sina_finance_spider(code, 3)
    eastmoney_guba_spider(code, 3)
    time.sleep(5)
    print("股票舆情数据爬取完成。")
    eastmoney_guba_spider('sh000001', 1)
    print("全部数据爬取完成。")
    cal_comment_score('guba')
    cal_comment_score('news')
    generate_report(code)


if __name__ == '__main__':
    print(datetime.now())
    process_data('sh688180')
    print(datetime.now())
