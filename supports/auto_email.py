# coding: utf-8

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

####################################################################################################
# 邮件操作
####################################################################################################

class SendEmail:
    def __init__(self):
        self.SMTP = None
        self.port = None
        self.user = None
        self.passwd = None
        self.sender_name = None
        self.to_list = []
        self.cc_list = []
        self.subject = None
        self.content = None
        self.doc = None

    def send(self):
        '''
        发送邮件
        '''
        print('邮件发送中...')
        try:
            server = smtplib.SMTP_SSL(self.SMTP, port=self.port)
            server.login(self.user, self.passwd)
            server.sendmail("<%s>" % self.user, self.to_list + self.cc_list, self.get_attach())
            server.close()
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败")
            print(e)

    def get_attach(self):
        '''
        构造邮件内容
        '''
        attach = MIMEMultipart()
        if self.content is not None:
            # 添加邮件内容
            txt = MIMEText(self.content)
            attach.attach(txt)
        if self.subject is not None:
            # 主题,最上面的一行
            attach["Subject"] = self.subject
        if self.user is not None:
            # 显示在发件人
            attach["From"] = self.sender_name + "<%s>" % self.user
        if self.to_list:
            # 收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            # 抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            # 估计任何文件都可以用base64，比如rar等
            # 文件名汉字用gbk编码代替
            name = os.path.basename(self.doc).encode("gbk")
            f = open(self.doc, "rb")
            doc = MIMEText(f.read(), "base64", "gb2312")
            doc["Content-Type"] = 'application/octet-stream'
            doc["Content-Disposition"] = 'attachment; filename="' + name + '"'
            attach.attach(doc)
            f.close()
        return attach.as_string()

def email_create(SMTP, port, user, password):
    se = SendEmail()
    se.SMTP = SMTP
    se.port = port
    se.user = user
    se.passwd = password
    return se

def send(se, sendername, to_list, cc_list, subject, content):
    se.sender_name = sendername
    se.to_list = to_list
    if cc_list:
        se.cc_list = cc_list
    # 主题
    se.subject = subject
    # 内容
    se.content = '\n' + content
    # 附件
    # se.doc = '填写一个文件路径'
    se.send()

if __name__ == '__main__':
    se = email_create("smtp", "port", "user", "password")
    send(se, "sendername", "to_list", "cc_list", "subject", 'content')