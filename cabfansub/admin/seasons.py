from flask import json, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, validators
from cabfansub.database import Season, Anime
from cabfansub.config import Config
from cabfansub.admin.authentication import need_to_login

config = Config()


@need_to_login
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
        return json.jsonify(result = "success", internalId = obj.id)
    else:
        return json.jsonify(result = "Invalid form data")


@need_to_login
def seasons():
    seasons = Season.select()
    return render_template("admin/seasons.html", seasons = seasons)


@need_to_login
def season_list_anime(id):
    season = Season.get(Season.id == id)
    anime = Anime.select().where(Anime.season == season)
    return render_template("admin/season_list_anime.html", season = season, anime = anime)


urlMapping = [
    ("/season/<int:id>", ["GET"], season_list_anime),
    ("/seasons", ["GET"], seasons),
    ("/ajax/add_season", ["POST"], add_season)
]
