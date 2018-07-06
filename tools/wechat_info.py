# -*- coding: utf-8 -*-
# @Time    : 2018/7/6 19:01
# @Author  : Woko
# @File    : wechat_info.py


import itchat
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def login(hotReload=True):
    itchat.auto_login(hotReload=hotReload)  # 实现登录状态保留，使你不用每运行一次就要扫一次二维码,默认是FALSE
    itchat.dump_login_status()
    print '登陆成功'


def get_all_user_sex():
    friends = itchat.get_friends(update=True)[:]
    total = len(friends) - 1
    man = women = other = 0

    for friend in friends[0:]:
        sex = friend["Sex"]
        if sex == 1:
            man += 1
        elif sex == 2:
            women += 1
        else:
            other += 1

    print "男性好友：%.2f%%, %d人" % ((float(man) / total * 100), man)
    print "女性好友：%.2f%%, %d人" % ((float(women) / total * 100), women)
    print "其他：%.2f%%, %d人" % ((float(other) / total * 100), other)


def get_chatroom_sex(chatroom_name):
    room = itchat.search_chatrooms(chatroom_name)
    if not room:
        return '没有找到该群'
    if len(room) > 1:
        print '找到了%d个符合条件的群，取第一个了哈' % len(room)
    room = room[0]
    itchat.update_chatroom(userName=room['UserName'], detailedMember=True)
    room = itchat.search_chatrooms(chatroom_name)
    room = room[0]
    members = room['MemberList']
    # print members
    man = women = other = 0
    total = len(members)
    print '群里一共%d人' % total
    for user in members:
        sex = user['Sex']
        if sex == 1:
            man += 1
        elif sex == 2:
            women += 1
        else:
            other += 1

    print '群名称：%s，总人数%d' % (room['NickName'], total)
    print "男性：%d人, %.2f%%" % (man, (float(man) / total * 100))
    print "女性：%d人, %.2f%%" % (women, (float(women) / total * 100))
    print "其他：%d人, %.2f%%" % (other, (float(other) / total * 100))


def get_contacts():
    contacts = itchat.get_contact()
    return contacts


if __name__ == '__main__':
    login()
    get_chatroom_sex('满天星')
