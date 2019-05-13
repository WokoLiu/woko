# -*- coding: utf-8 -*-
# @Time    : 2019-05-13 21:39
# @Author  : Woko
# @File    : ziroom_release.py

import time
import logging
import requests
from tools.server_chan import wechat


def get_headers():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'}


def refresh(room_id, house_id):
    url = 'http://www.ziroom.com/detail/info'
    params = {
        'id': room_id,
        'house_id': house_id,
    }
    try:
        response = requests.get(url, params=params, headers=get_headers())
    except requests.RequestException as e:
        logging.error(e)
        return {}

    try:
        res = response.json()
    except TypeError as e:
        logging.error(e)
        return {}
    if res.get('code') != 200:
        logging.error(res)
        return {}
    air_part = res.get('data', {}).get('air_part', {})
    if not air_part:
        return {}
    info = air_part['air_quality']['show_info']
    is_pass = info['show_type']
    if is_pass == 'pass':
        # alert
        notify(house_id)
    elif is_pass == 'nopass':
        print('nopass')
    else:
        # need to update this script
        wechat('ziru_release bug', '')


def notify(house_id):
    url = f'http://www.ziroom.com/z/vh/{house_id}.html'
    desp = f'[房间链接]({url})'
    wechat('有个房子已经释放啦', desp=desp)


def run(room_id, house_id):
    while 1:
        refresh(room_id, house_id)
        time.sleep(300)


if __name__ == '__main__':
    room_id = '0'
    house_id = '0'
    res = refresh(room_id, house_id)
    print(res)