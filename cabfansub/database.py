import json

from flask import session
from peewee import *
from playhouse.fields import PasswordField
from flask_babel import gettext
from cabfansub.config import Config
from cabfansub.common import genRandomString, utcNow

database = MySQLDatabase(host = Config.DB_HOST,
                         user = Config.DB_USER,
                         password = Config.DB_PASSWORD,
                         database = Config.DB_NAME,
                         fields = {"JSON": "varchar"})


class JSONField(Field):
    db_field = "longtext"

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        return json.loads(value)


def create_all_tables():
    database.create_tables(
        [User, Anime, Episode, Tag, AnimeTagMap, Season, ForgotToken, LoginToken],
        safe = False)


class BaseModel(Model):
    class Meta:
        database = database


class IncorrectPassword(Exception):
    pass


class User(BaseModel):
    # auto id field
    username = CharField()
    real_name = CharField(default = gettext("Anonymous"))
    email = CharField()
    password = PasswordField()
    avatar = CharField(default = "noavatar.png")
    role = CharField(default = gettext("Admin"))
    description = TextField(default = gettext("No description"))

    def login(self, password):
        if not self.password.check_password(password):
            raise IncorrectPassword
        return LoginToken.new(self.id)

    @staticmethod
    def logout():
        session.clear()


class InvalidToken(Exception):
    pass


class LoginToken(BaseModel):
    token_key = CharField(primary_key = True, max_length = 32)
    token_hash = PasswordField()
    user_id = ForeignKeyField(rel_model = User, to_field = 'id')

    @staticmethod
    def new(user_id):
        token_key = genRandomString(32)
        token_value = genRandomString(128)
        LoginToken.create(token_key = token_key, token_hash = token_value, user_id = user_id)
        return token_key, token_value

    @staticmethod
    def use(token_key, token_value):
        try:
            token_obj = LoginToken.get(LoginToken.token_key == token_key)
        except DoesNotExist:
            raise InvalidToken
        if not token_obj.token_hash.check_password(token_value):
            raise InvalidToken
        return token_obj.user_id


class ForgotToken(BaseModel):
    token = CharField(primary_key = True, default = lambda: genRandomString(128), max_length = 128)
    timestamp = DateTimeField(default = utcNow())
    user_id = ForeignKeyField(rel_model = User, to_field = 'id')

    @staticmethod
    def new(user_id):
        ForgotToken.delete().where(ForgotToken.user_id == user_id).execute()
        token = ForgotToken.create(user_id = user_id)
        return token


class Season(BaseModel):
    # auto id field
    season_name = CharField(unique = True)
    year = IntegerField()


class Anime(BaseModel):
    # auto id field
    anime_name = CharField()
    season = ForeignKeyField(rel_model = Season, to_field = "id")
    metadata = JSONField()
    # {
    #   type: TV / Bluray / OVA / OVN / ...
    #   episodes: number of episodes
    #   ... added later
    # }


class Episode(BaseModel):
    # auto id field
    anime = ForeignKeyField(rel_model = Anime, to_field = "id")
    episode_number = IntegerField()
    metadata = JSONField()
    # broadcast_date = DateTimeField()
    # length = SmallIntegerField()
    # status = CharField()
    link = JSONField(default = {})
    # {
    #   "Magnet": <link>,
    #   ...
    # }


class Tag(BaseModel):
    # auto id field
    tag_name = CharField()
    description = CharField(default = "")


class AnimeTagMap(BaseModel):
    tag_id = ForeignKeyField(rel_model = Tag, to_field = "id")
    anime_id = ForeignKeyField(rel_model = Anime, to_field = "id")


class Setting(BaseModel):
    key = CharField(unique = True)
    value = JSONField()

    def __getitem__(self, key):
        try:
            entry = Setting.get(Setting.key == key)
        except Setting.DoesNotExist:
            raise KeyError
        return entry.value

    def __setitem__(self, key, value):
        entry, _ = Setting.get_or_create(key = key)
        entry.value = value
        entry.save()

    def __delitem__(self, key):
        try:
            entry = Setting.get(Setting.key == key)
        except Setting.DoesNotExist:
            raise KeyError
        entry.delete_instance()
