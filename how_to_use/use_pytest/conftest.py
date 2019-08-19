# -*- coding: utf-8 -*-
# @Time    : 2018/10/4 14:56
# @Author  : Woko
# @File    : conftest.py

import pytest


@pytest.fixture(scope='module', params=['q', pytest.param('w', marks=pytest.mark.skip)])
def old_dict(request):
    return {
        'a': 1,
        'b': request.param,
        'c': 3,
    }


# scope must be function?
@pytest.fixture(params=['1', '2'])
def just_fixture(request):
    print('just fixture' + request.param)


# set up and tear down
@pytest.fixture(params=[1, 2])
def just_session(request):
    print('set up')
    yield request.param
    print('tear down')
