# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 22:24
# @Author  : Woko
# @File    : blame_someone.py

"""
if we got an error on project
get the error line and send an email to it's author
"""

import datetime
import subprocess
from email.mime.text import MIMEText
from email.header import Header
from tools.email_tool import TencentExEmail


class BlameInfo(object):
    """contain everything about git blame"""
    def __init__(self, author, author_mail, author_time, author_tz,
                 committer, committer_mail, committer_time, committer_tz,
                 summary, filename, line_no):
        self.author = author
        self.author_mail = author_mail
        self.author_time = author_time
        self.author_tz = author_tz
        self.committer = committer
        self.committer_mail = committer_mail
        self.committer_time = committer_time
        self.committer_tz = committer_tz
        self.summary = summary
        self.filename = filename
        self.ling_no = line_no

    def __bool__(self):
        if not self.author or not self.committer:
            return False
        else:
            return True


def get_author(file_path, line_no) -> BlameInfo:
    """get git blame info from file"""
    try:
        # use universal_newlines to make sure it returns a str instead of a bytes
        # pass encoding='utf-8' to subprocess.Popen() and use it in _translate_newlines()
        # otherwise it will decode `file_data` with ascii and raise a UnicodeDecodeError
        file_data = subprocess.check_output(
            ['git', 'blame', '-p', '-L', '{l},{l}'.format(l=line_no), file_path],
            universal_newlines=True, stderr=subprocess.STDOUT, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        # do something
        raise e

    blame_info = {}
    # todo bad way to get info
    for line in file_data.split('\n')[1:-2]:
        k, v = line.split(' ', 1)
        print(k, v)
        blame_info[k.replace('-', '_')] = v

    return BlameInfo(**blame_info, line_no=line_no)


def make_blame_email(blame: BlameInfo, detail):
    """build text email by BlameInfo"""
    format_time = lambda timestamp: datetime.datetime.fromtimestamp(int(timestamp))
    text = ('There is an error on {file}:{line},'
            ' which was written by {author} at {time1} and committed by {committer} at {time2}.'
            ' Here is the error details \n{detail}'
            .format(file=blame.filename, line=blame.ling_no, author=blame.author,
                    committer=blame.committer, time1=format_time(blame.author_time),
                    time2=format_time(blame.committer_time), detail=detail))
    message = MIMEText(text, _charset='utf-8')
    message['Subject'] = 'Error!'
    message['From'] = (Header('woko/blame', 'utf-8').encode('utf-8'))
    message['To'] = ','.join((blame.author_mail, blame.committer_mail))
    return message


def send_blame_email(email_name, email_pswd, file_path, line_no, detail):
    """like run(), send an email to error codes' author and committer"""
    try:
        blame_info = get_author(file_path, line_no)
        if not blame_info:
            raise Exception('can\'t get file author')
    except Exception as e:
        print(e.args)
        return None

    mail = TencentExEmail(email_name, email_pswd)

    message = make_blame_email(blame_info, detail)

    res = mail.send_text([blame_info.author_mail, blame_info.committer_mail], message)
    print(res)
    return res


if __name__ == '__main__':
    my_email = 'woko@example.com'
    my_email_pswd = 'wokopswd'
    file_path = './count_git_line.py'
    error_line = 10
    detail = 'this is the error msg'
    send_blame_email(my_email, my_email_pswd, file_path, error_line, detail)
