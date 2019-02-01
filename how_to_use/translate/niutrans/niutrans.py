# -*- coding: utf-8 -*-

"""使用小牛翻译，翻译文档"""

import requests


def translate(src_text):
    if not src_text:
        return ''
    url = 'http://api.niutrans.vip/NiuTransServer/translation'
    params = {
        'from': 'en',
        'to': 'zh',
        'apikey': 'my_apikey',
        'src_text': src_text
    }
    response = requests.post(url, data=params)
    res = response.json()
    return res['tgt_text']


def trans(text):
    result = []
    for garagraph in text:
        tmp = []
        for line in garagraph:
            tmp.append(translate(line))
        result.append(tmp)
    return result


def get_file(filepath):
    result = []
    with open(filepath, 'r') as f:
        for line in f:
            result.append(split(line))
    return result


def write_file(filepath, result):
    with open(filepath, 'w') as f:
        for paragraph in result:
            for line in paragraph:
                f.write(line)
            f.write('\n')


def split(paragraph):
    tmp_paragraph = []
    for line in paragraph.split('.'):
        tmp_paragraph.append(line.strip())
    return tmp_paragraph


if __name__ == '__main__':
    read_path = './file.txt'
    result_path = './result.txt'
    text = get_file(read_path)
    result = trans(text)
    write_file(result_path, result)
    # print trans('hello')