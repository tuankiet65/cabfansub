from flask import json
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, validators
from cabfansub.database import Season, database
from cabfansub.config import Config

config = Config()


def add_season():
    class AddSeasonForm(FlaskForm):
        season_name = SelectField("Season name",
                                  choices = [("Spring", "Spring"),
                                             ("Summer", "Summer"),
                                             ("Autumn", "Autumn"),
                                             ("Winter", "Winter")])
        year = IntegerField("Year", validators = [validators.DataRequired()])

    form = AddSeasonForm()
    if form.validate_on_submit():
        obj, created = Season.get_or_create(season_name = "{} {}".format(form.data['season_name'], form.data['year']),
                          year = form.data['year'])
        if not created:
            return json.jsonify(result = "Season already exists")
        return json.jsonify(result = "success", internalId=obj.id)
    else:
        return json.jsonify(result = "Invalid form data")


urlMapping = [
    ("/ajax/add_season", ["POST"], add_season)
]
