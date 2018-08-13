# -*- coding: utf-8 -*-
# @Time    : 2018/7/6 19:01
# @Author  : Woko
# @File    : wechat_info.py


from collections import defaultdict
import sys
import itchat

reload(sys)
sys.setdefaultencoding('utf-8')


def login(hotReload=True):
    itchat.auto_login(hotReload=hotReload)  # 实现登录状态保留，使得不用每运行一次就要扫一次二维码,默认是FALSE
    itchat.dump_login_status()
    print '登陆成功'


def get_all_user_sex():
    """计算所有好友的性别比"""
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


def search_first_chatroom(chatroom_name):
    """根据群名称搜索群聊，并返回第一个"""
    room = itchat.search_chatrooms(chatroom_name)
    if not room:
        return None
    if len(room) > 1:
        print '找到了%d个符合条件的群，取第一个了哈' % len(room)
    room = room[0]
    itchat.update_chatroom(userName=room['UserName'], detailedMember=True)
    return itchat.search_chatrooms(userName=room['UserName'])


def get_chatroom_sex(chatroom_name):
    """计算某个群里的性别比"""
    room = search_first_chatroom(chatroom_name)
    if not room:
        print '没有找到该群'
        return None
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


def get_chatroom_friends(chatroom_name):
    """获得某个群里自己的好友"""
    room = search_first_chatroom(chatroom_name)
    if not room:
        print '没有找到该群'
        return None
    members = room['MemberList']
    friends = get_friends()
    result = []
    for user in members:
        if user.UserName in friends:
            result.append(user)
    print '群名称：', room.NickName
    print '这个群里一共 %d 人是好友' % len(result)
    for one in result:
        print one.RemarkName, one.NickName
    return result


def get_friends():
    """获取自己全部好友"""
    contacts = itchat.get_friends(update=True)
    friends = defaultdict(str)
    for user in contacts:
        friends[user.UserName] = user.NickName
    return friends


if __name__ == '__main__':
    login()
    get_chatroom_friends('游泳群')
