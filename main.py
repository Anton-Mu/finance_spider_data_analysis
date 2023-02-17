from data_process.report_generate import generate_report
from data_process.score_store import cal_comment_score
from spider.eastmoney_guba import eastmoney_guba_spider
from spider.sina_finance import sina_finance_spider
from datetime import datetime


def main():
    sina_finance_spider('sh688180', 3)
    eastmoney_guba_spider('sh688180', 3)
    eastmoney_guba_spider('sh000001', 1)
    cal_comment_score('guba')
    cal_comment_score('news')
    generate_report('sh688180')


if __name__ == '__main__':
    print(datetime.now())
    main()
    print(datetime.now())

