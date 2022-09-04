from datetime import datetime
from flask import request
from flask_jwt_extended import create_access_token
from passlib.context import CryptContext

from apis import users_collection
from apis.utils import responses
from apis.utils.error_logger import logger

from . import main


BASE_URL = '/auth'

pwd_hasher = CryptContext(schemes=['sha256_crypt'])


@main.route(f"{BASE_URL}/register", methods=['POST'])
def register_user_route():
    try:
        data = request.get_json()

        new_user = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password_hash': pwd_hasher.hash(data['password']),
            'date_joined': datetime.utcnow()
        }

        # check if user exists
        user_doc = users_collection.find_one({'email': new_user['email']})
        if user_doc:
            return responses.http_response_409({
                'status': 'failed',
                'msg': 'Email already exists!'
            })

        # if user does not exists create new user
        users_collection.insert_one(new_user)

        return responses.http_response_200({
            'status': 'success',
            'msg': 'Account created!'
        })
    except Exception as e:
        logger.error('register_user_route@Error')
        logger.error(e)
        return responses.http_response_500({
            'status': 'failed',
            'msg': 'An error occurred!'
        })


@main.route(f'{BASE_URL}/login', methods=['POST'])
def login_route():
    try:
        data = request.get_json()

        user = {
            'email': data['email'],
            'password': data['password']
        }

        # retrieve user from db
        user_exists = users_collection.find_one({'email': user['email']})

        if not user_exists:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'Email does not exists!'
            })

        # validate user password
        valid_pwd = pwd_hasher.verify(user['password'], user_exists['password_hash'])

        if not valid_pwd:
            return responses.http_response_401({
                'status': 'failed',
                'msg': 'Invalid credentials!'
            })

        # create access token
        access_token = create_access_token(identity=user_exists['email'])

        return responses.http_response_200({
            'status': 'success',
            'msg': 'Login successful!',
            'access_token': access_token
        })
    except Exception as e:
        logger.error('login_route@Error')
        logger.error(e)
        return responses.http_response_500({
            'status': 'failed',
            'msg': 'An error occurred!'
        })
