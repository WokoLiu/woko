# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 18:10
# @Author  : Woko
# @File    : email_tool.py

"""send email from tecent exmail"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

text = 'test email from python.'

msg = MIMEText(text, _charset='utf-8')


class TencentExEmail(object):
    """send email by Tencent Exmail"""
    def __init__(self, email, pswd):
        self.from_email = email
        self.pswd = pswd
        # check on http://service.exmail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1000585
        self._send_server_host = 'smtp.exmail.qq.com'
        self._send_server_port = 465

    def send_text(self, to_email_list: list, message):
        with smtplib.SMTP_SSL(self._send_server_host, self._send_server_port) as server:
            # server.set_debuglevel(1)
            server.login(self.from_email, self.pswd)
            res = server.sendmail(self.from_email, to_email_list, message.as_string())
        return res


if __name__ == '__main__':
    username = 'woko@mycorp.com'
    password = 'mypassword'
    email = TencentExEmail(username, password)
    to_email = '123@qq.com'
    to_email2 = '456@qq.com'

    text = 'email test'
    message = MIMEText(text, _charset='utf-8')
    message['Subject'] = 'subject test'
    # 'From' can be only emailaddr or 'name <emailaddr>', we can use email.utils.formataddr
    message['From'] = formataddr((Header('啦啦啦', 'utf-8').encode('utf-8'), username))
    # message['To'] = formataddr((Header('bamboo', 'utf-8').encode('utf-8'), to_email2))
    message['To'] = ','.join((to_email, to_email2))

    print(message)
    res = email.send_text([to_email, to_email2], message)
    print(res)
