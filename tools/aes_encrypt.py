# -*- coding: utf-8 -*-
# @Time    : 2017/10/30 20:09
# @Author  : Woko
# @File    : aes_encrypt.py

import sys
# 这里是为了兼容Python2，才做的这么麻烦
if sys.version_info[0] > 2:
    import crypto
    sys.modules['Crypto'] = crypto

    # todo bytes 和 str 转换的问题，真的好麻烦啊
    def hex_encode(x):
        if isinstance(x, str):
            return bytes(x, encoding='utf-8').hex()
        else:
            return x.hex()
    hex_decode = lambda x: bytes.fromhex(x)
    make_str = lambda x: str(x, encoding='utf-8')
else:
    hex_encode = lambda x: x.encode('hex')
    hex_decode = lambda x: x.decode('hex')
    make_str = str

from Crypto.Cipher import AES

__all__ = ['AesEncrypt']


class AesEncrypt(object):
    """AES-128"""
    key_size = AES.key_size

    def __init__(self, key, mode=AES.MODE_ECB, IV=''):
        self.key = key
        self.mode = mode
        # self.IV = AES.block_size * '\0'
        self.IV = IV

    def __pad(self, text):
        # BS = AES.block_size
        # pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        length = AES.block_size
        count = len(text)
        if count < length:
            add = (length - count)
            text += (chr(add) * add)
        return text

    def __unpad(self, text):
        # unpad = lambda s: s[0:-ord(s[-1])]
        text = make_str(text)
        return text[0:-ord(text[-1])]

    def encrypt(self, text, upper=True):
        cryptor = AES.new(self.key, self.mode, IV=self.IV)  # 必须每次重新new，不能重复使用
        text = self.__pad(text)
        res = hex_encode(cryptor.encrypt(text))
        if upper:
            return res.upper()
        return res

    def decrypt(self, text):
        # 这里有可能会出现异常，建议放在外层catch
        cryptor = AES.new(self.key, self.mode, IV=self.IV)
        res = cryptor.decrypt(hex_decode(text))
        res = self.__unpad(res)
        return res

if __name__ == '__main__':
    key = 'qwertyuiopasdfgh'
    encryptor = AesEncrypt(key)
    a = encryptor.encrypt('yoyoo')
    print(a)
    print(encryptor.decrypt(a))
