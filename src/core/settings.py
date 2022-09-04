from datetime import timedelta

from dotenv import dotenv_values


env_config = dotenv_values('.env.dev')


class BaseConfig:
    Debug = True

    JWT_ACCESS_CSRF_HEADER_NAME = "csrf_token"
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_CSRF_IN_COOKIES = False
    JWT_HEADER_TYPE = "Bearer"
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(env_config['TOKEN_EXPIRY_TIME']))
    JWT_TOKEN_LOCATION = ["headers", "cookies"]

    MONGODB_URI = env_config['MONGODB_URI']
    SECRET_KEY = env_config['SECRET_KEY']


class DevelopmentConfig(BaseConfig):
    JWT_REFRESH_TOKEN_EXPIRES = False


class ProductionConfig(BaseConfig):
    pass


config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
