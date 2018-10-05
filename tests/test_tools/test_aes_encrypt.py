# -*- coding: utf-8 -*-
# @Time    : 2018/10/6 00:32
# @Author  : Woko
# @File    : test_aes_encrypt.py

import random
import string
import pytest
from tools.aes_encrypt import AesEncrypt, make_str, make_bytes


@pytest.fixture(params=[''.join(random.sample(string.ascii_letters,
                                              random.choice(AesEncrypt.key_size)))
                        for _ in range(5)])
def key(request):
    return request.param


@pytest.fixture(params=[''.join(random.sample(string.ascii_letters,
                                              random.randint(0, len(string.ascii_letters))))
                        for _ in range(5)])
def text(request):
    return request.param


class TestAesEncrypt(object):
    def test_upper(self, key, text):
        aes_encryptor = AesEncrypt(key)

        a = aes_encryptor.encrypt(text)
        assert a.isupper()

        b = aes_encryptor.encrypt(text, upper=False)
        assert b.islower()

    def _encode(self, key, text):
        aes_encryptor = AesEncrypt(key)

        code = aes_encryptor.encrypt(text)
        res = aes_encryptor.decrypt(code)
        assert isinstance(res, str)
        assert res == make_str(text)

    def test_bytes(self, key, text):
        bytes_key = make_bytes(key)
        bytes_text = make_bytes(text)
        self._encode(key, text)
        self._encode(bytes_key, text)
        self._encode(key, bytes_text)
        self._encode(key, bytes_text)

    @pytest.mark.skip
    def test_mode(self, key, text):
        pass
