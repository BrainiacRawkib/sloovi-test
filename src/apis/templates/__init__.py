from flask import Blueprint


templates = Blueprint('templates', __name__)

from . import routes
