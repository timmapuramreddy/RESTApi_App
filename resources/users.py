# import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='This field cannot be blank!!')
    parser.add_argument('password',
        type=str,
        required=True,
        help='This field cannot be blank!!')
    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {'Error': 'User already registered!!!'}, 400
        else:
            user = UserModel(**data)
            user.save_to_db()
            return {'message': 'user registered successfully !!!'}, 201

        # return msg, 400 if user else 201
