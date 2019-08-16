# -*- coding: utf-8 -*-
# @Time    : 2019-08-16 10:46
# @Author  : Woko
# @File    : cipher.py


import binascii
import hashlib
import os
from typing import AnyStr
from tools.aes_encrypt import AesEncrypt


class Cipher:
    """密码加密算法"""
    HASH = 'SHA256'
    TIMES = 10000

    @staticmethod
    def pbkdf2_encode(base_pswd: bytes, salt: AnyStr = None) -> (str, str):
        if salt and isinstance(salt, str):
            salt = binascii.unhexlify(salt)
        if not salt:
            salt = os.urandom(32)

        pswd = hashlib.pbkdf2_hmac(Cipher.HASH, base_pswd, salt,
                                   Cipher.TIMES)  # 随机生成盐值
        pswd_str = binascii.hexlify(pswd).decode()
        salt_str = binascii.hexlify(salt).decode()
        return pswd_str, salt_str

    @staticmethod
    def aes_decode(key: AnyStr, text: AnyStr):
        try:
            return AesEncrypt(key).decrypt(text)
        except Exception:
            raise
