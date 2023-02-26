# financial-spider-data-analysis
# 金融爬虫与数据分析
本项目功能为爬取指定股票的新浪财经数据与东方财富股吧舆论数据，作情感分析与数据分析后，自动生成docx格式分析报告，并发送至指定邮箱。
本项目录制了配套视频讲解教程，发布在b站上，地址为：
1.爬虫部分：https://www.bilibili.com/video/BV19D4y1g7Yp/?spm_id_from=333.999.0.0&vd_source=6aacace1780d48191a4d50dd173ad887
2.数据分析与存储部分：正在制作中...

## 使用方法
### 本地运行

在执行程序前，需要在以下文件中配置相关参数：
- tools/config.py
```
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
```

其中，数据库应按照如下结构建立：
![image](https://github.com/Anton-Mu/finance_spider_data_analysis/blob/main/guba_struc.png)
![image](https://github.com/Anton-Mu/finance_spider_data_analysis/blob/main/sina_struc.png)
![image](https://github.com/Anton-Mu/finance_spider_data_analysis/blob/main/ua_struc.png)
其中，数据库ua_pool为用于生成随机请求头user_agent的库，需要在建立完成数据库后导入位于文件根目录下的```ua_pool.sql```文件数据。

如果需要实现邮件发送功能，则还需要配置如下参数：
- data_process/email_send.py
```
import smtplib  
from email.mime.application import MIMEApplication  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
  
  
def send_email():  
    user = '发件人邮箱@qq.com'  
    pwd = 'QQ邮箱的SMTP授权码'  
    to = '收件人邮箱@qq.com'  
    ...
```

在完成上述配置后，运行```data_process/whole_process.py```即可自动开始爬取分析，并生成分析报告。分析报告位于```docs```文件夹下。修改该文件中```process_data```函数参数为其他股票代码，即可对其他指定股票进行爬取分析工作。例如，对于隆基股份则应在```data_process/whole_process.py```中执行
```
process_data('sh601012')
```

### 服务器部署

该部分说明后续更新。

## 注意事项
1. 搭建数据库时应与上述图片内结构相同。由于数据库查重功能部分依赖数据库中键的设置实现，因此改变结构可能导致程序部分功能出错。
2. 数据爬取分析与报告生成的运行最佳时间为晚间18:00-23:00间，数据采集相对更加全面有效。
3. 如果手动高频爬取东方财富股吧数据，可能导致服务器暂时封禁ip。可以自行挂代理或者等待一段时间后再次尝试。
