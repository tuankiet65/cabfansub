import os

from cabfansub.common import genRandomString


class EC2ProductionConfig(object):
    SECRET_KEY = genRandomString(256)
    DEBUG = False
    PROPAGATE_EXCEPTIONS = False
    SERVER_NAME = "e3.tuankiet65.moe"
    ROOT_FOLDER = "/home/ubuntu/cabfansub/cabfansub/"
    PREFERRED_URL_SCHEME = "https"

class OpenShiftProductionConfig(object):
    pass

class DevelopmentConfig(object):
    SECRET_KEY = "Well, this is supposed to be secret and random, " \
                 "but in development environment, who cares?"
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    SERVER_NAME = "localhost:5000"
    ROOT_FOLDER = "/home/tuankiet65/PycharmProjects/cabfansub/cabfansub/"
    PREFERRED_URL_SCHEME = "http"

    DB_HOST = "localhost"
    DB_NAME = "cfs"
    DB_USER = "cfs"
    DB_PASSWORD = "cfs"


class Config(DevelopmentConfig):
    PORT = 5000

    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPCHA_PUBLIC_KEY")
    RECAPTCHA_SECRET_KEY = os.getenv("RECAPCHA_SECRET_KEY")
    HUMMINGBIRD_CLIENT_ID = os.getenv("HUMMINGBIRD_CLIENT_ID")

    def __init__(self):
        self.ANIME_POSTER_FOLDER = os.path.join(self.ROOT_FOLDER, "static/img/anime/poster")
        self.ANIME_COVER_FOLDER = os.path.join(self.ROOT_FOLDER, "static/img/anime/cover")