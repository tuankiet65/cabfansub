from flask import json
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, validators
from cabfansub.database import Season, database
from cabfansub.config import Config

urlMapping = [
]
