from flask import Blueprint
from cabfansub.config import Config

config = Config()

ajax = Blueprint('ajax', __name__, url_prefix="/ajax")