# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 13:58
# @Author  : Woko
# @File    : genereate_rsa_keys.py

"""generate a pear of rsa private/public key

how to do it on linux:
$ ssh-keygen -t rsa -b 2048 -f private.pem
$ openssl rsa -pubout -outform PEM -in private.pem -out public.pem
$ rm private.pem.pub
"""

import rsa


def assert_str(text):
    """make sure it's str"""
    if isinstance(text, bytes):
        return str(text, encoding='utf-8')
    else:
        return str(text)


# generate a pare of rsa public/private keys with 2048 bits
(public_key, private_key) = rsa.newkeys(2048)

# change it to bytes
public = public_key.save_pkcs1()
private = private_key.save_pkcs1()

# change it to str
public = assert_str(public)
private = assert_str(private)

print(type(public), public)
print(type(private), private)

# write to file
with open('public.pem', 'w') as f:
    f.write(public)

with open('private.pem', 'w') as f:
    f.write(private)

# read from file
with open('public.pem') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open('private.pem') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())
