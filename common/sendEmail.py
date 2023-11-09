import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.readConfig import ReadConfig

# 实例化
rc = ReadConfig()

class SendEmail:

    def __init__(self):
        # 配置邮箱属性
        # 发送邮件
        self.sender = rc.get_config("email", "sender")
        # 接收邮箱
        self.receiver = eval(rc.get_config("email", "receiver"))
        # 发送邮件主题
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.subject = '自动化测试报告' + t
        # 发送邮箱服务器
        self.smtpserver = rc.get_config("email", "smtpserver")
        # 发送邮箱用户/授权码
        self.username = rc.get_config("email", "sender")
        self.password =rc.get_config("email", "password")

    def __config(self, file):
        # 读取html文件内容
        with open(file, 'rb') as f:
            mail_body = f.read()
            # 组装邮件内容
            msg = MIMEMultipart()
            # 添加附件内容
            att = MIMEText(mail_body, 'plain', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Dispostion"] = 'attachment; filename=report.zip'
            msg.attach(att)
            # 添加邮件的文本内容
            content = '自动化测试报告详情，请查收附件'
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            msg['Subject'] = Header(self.subject, 'utf-8')
            msg['From'] = self.sender
            msg['To'] = ",".join(self.receiver)
        return msg

    def send(self, file):
        # 第二步：准备附件
        msg = self.__config(file)
        # 第三步：登录并发送邮件
        try:
            # 1--实例化smtp类
            smtp = smtplib.SMTP()
            # 2--连接stmp服务器
            smtp.connect(self.smtpserver)
            # 3--登录邮箱
            smtp.login(self.username, self.password)
            # 4--设置发送人，收件人，邮件内容
            smtp.sendmail(self.sender, self.receiver, msg.as_string())
        except Exception as msg:
            print("邮件发送失败！", msg)
        else:
            print("邮件发送成功！")
        finally:
            smtp.quit()

if __name__ == '__main__':
    se = SendEmail()
    se.send(r"/Users/liusha/PycharmProjects/pythonProject_InterfaceTest/testReport/temp/测试报告.zip")
