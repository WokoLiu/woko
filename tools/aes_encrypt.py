# -*- coding: utf-8 -*-
# @Time    : 2017/10/30 20:09
# @Author  : Woko
# @File    : aes_encrypt.py

import sys

# 这里是为了兼容Python2，才做的这么麻烦
if sys.version_info[0] > 2:
    def make_str(value):
        if isinstance(value, bytes):
            return str(value, encoding='utf-8')
        else:
            return str(value)


    def make_bytes(value):
        if isinstance(value, str):
            return bytes(value, encoding='utf-8')
        else:
            return bytes(value)


    hex_encode = lambda x: x.hex()  # input must be bytes
    hex_decode = lambda x: bytes.fromhex(x)  # input must be str
else:
    hex_encode = lambda x: x.encode('hex')
    hex_decode = lambda x: x.decode('hex')
    make_str = str
    make_bytes = bytes

from Crypto.Cipher import AES

__all__ = ['AesEncrypt']


class AesEncrypt(object):
    """AES-128"""
    key_size = AES.key_size

    def __init__(self, key, mode=AES.MODE_ECB, **kwargs):
        self.key = make_bytes(key)
        self.mode = mode
        # self.IV = AES.block_size * '\0'
        self._kwargs = kwargs

    def __pad(self, text):
        # BS = AES.block_size
        # pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        text = make_str(text)
        length = AES.block_size
        count = len(text) % length
        if count < length:
            add = (length - count)
            text += (chr(add) * add)
        return text

    def __unpad(self, text):
        # unpad = lambda s: s[0:-ord(s[-1])]
        text = make_str(text)
        return text[0:-ord(text[-1])]

    def encrypt(self, text, upper=True):
        # 必须每次重新new，不能重复使用
        cryptor = AES.new(self.key, self.mode, **self._kwargs)
        text = self.__pad(text)
        res = hex_encode(cryptor.encrypt(make_bytes(text)))
        if upper:
            return res.upper()
        return res

    def decrypt(self, text):
        # 这里有可能会出现异常，建议放在外层catch
        cryptor = AES.new(self.key, self.mode, **self._kwargs)
        text = make_str(text)
        res = cryptor.decrypt(hex_decode(text))
        res = self.__unpad(res)
        return res
