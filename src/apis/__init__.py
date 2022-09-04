from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient

from core import settings
from core.settings import config


jwt = JWTManager()

# initialize mongo db config
mongo_host_uri = settings.BaseConfig.MONGODB_URI
mongo_client = MongoClient(settings.BaseConfig.MONGODB_URI)

# connect to db
db = mongo_client['sloovidb']

# collections
users_collection = db['users']
templates_collection = db.templates

API_PREFIX = '/api/v1'


def create_app(conf='dev'):
    app = Flask(__name__)

    # CORs config
    CORS(app)

    app.config.from_object(config[conf])

    # JWT config
    jwt.init_app(app)

    # Registered Blueprints

    from apis.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix=f'{API_PREFIX}')

    from apis.templates import templates as templates_blueprint
    app.register_blueprint(templates_blueprint, url_prefix=f'{API_PREFIX}')

    # Rate limiter config
    Limiter(
        app,
        key_func=get_remote_address,
        default_limits=['6 per minute', '30 per hour']
    )

    return app
