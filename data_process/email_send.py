import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email():
    user = 'userexample@qq.com'
    pwd = 'pwd'
    to = 'toexample@qq.com'

    msg = MIMEMultipart()

    mail_msg = '''
    <p>每日舆情分析报告</p>
    '''
    msg.attach(MIMEText(mail_msg, 'html', 'gbk'))

    # att1 = MIMEText(open('../docs/舆情分析报告.docx', encoding='gbk').read(), 'base64', 'utf-8')
    with open('../docs/舆情分析报告.docx', 'rb') as f:
        att1 = MIMEApplication(f.read(), _subtype='docx')
    att1['Content-Type'] = 'application/octet-stream'
    att1['Content-Disposition'] = 'attachment;filename="financial_analysis_report.docx"'
    msg.attach(att1)

    msg['Subject'] = '每日舆情分析报告'
    msg['From'] = user
    msg['To'] = to

    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    s.login(user, pwd)
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':
    send_email()
