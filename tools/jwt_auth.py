# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 14:22
# @Author  : Woko
# @File    : jwt_auth.py

import time
import jwt

# get keys
with open('public.pem') as f:
    public_key = f.read()
    # print(public_key)

with open('private.pem') as f:
    private_key = f.read()
    # print(private_key)

# make payload
now = int(time.time())
audience = '123'
exp = 1
alg = 'RS256'

payload = {
    'iat': now,
    'aud': audience,
    'exp': now + exp,
}

# encode
token = jwt.encode(payload, private_key, alg)
print(token)

# decode
data = jwt.decode(token, public_key, audience=audience)
print(data)

# don't verify exp
time.sleep(2)
data = jwt.decode(token, public_key, audience=audience, verify_expiration=False)
print(data)
