# -*- coding: utf-8 -*-
# @Time    : 2019-06-14 15:21
# @Author  : Woko
# @File    : restful.py

from flask_restful import Api, Resource, reqparse

api = Api()

data = ['Woko', 'Liu']


class User(Resource):

    def get(self, user_id: int = None):
        if user_id is None:
            return data

        try:
            return data[user_id]
        except IndexError:
            return 'no such user', 400

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='form')
        args = parser.parse_args()
        username = args.username

        if username in data:
            return 'duplicate username', 400
        data.append(username)
        return username


api.add_resource(User, '/users', '/users/<int:user_id>')
