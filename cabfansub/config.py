import os

from cabfansub.common import genRandomString


class EC2ProductionConfig(object):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = False
    SERVER_NAME = "e3.tuankiet65.moe"
    ROOT_FOLDER = "/home/ubuntu/cabfansub/cabfansub/"
    PREFERRED_URL_SCHEME = "https"

class OpenShiftProductionConfig(object):
    pass

class DevelopmentConfig(object):
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
    SECRET_KEY = genRandomString(256)

    PORT = 5000

    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPCHA_PUBLIC_KEY")
    RECAPTCHA_SECRET_KEY = os.getenv("RECAPCHA_SECRET_KEY")

    def __init__(self):
        self.EXPORT_FOLDER = os.path.join(self.ROOT_FOLDER, "static/export")
        self.AVATAR_FOLDER = os.path.join(self.ROOT_FOLDER, "static/avatar")