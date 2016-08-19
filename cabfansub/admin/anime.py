# Please, the plural form of 'anime' is 'anime', not 'animes', ok?

from wtforms import IntegerField, validators
from werkzeug.utils import secure_filename
from flask import json, render_template
from flask_wtf import FlaskForm
import requests
import mimetypes
import os
import tempfile
import shutil

from cabfansub.database import Season, Anime, Episode, Tag, AnimeTagMap, database
from cabfansub.config import Config
from cabfansub.admin.authentication import need_to_login

config = Config()


class HummingbirdAPI:
    def __init__(self, client_id):
        self.client_id = client_id

    def get_anime(self, anime_id, is_mal = False):
        if is_mal:
            anime_id = "myanimelist:{}".format(anime_id)
        print("https://hummingbird.me/api/v2/anime/{}".format(anime_id))
        req = requests.get("https://hummingbird.me/api/v2/anime/{}".format(anime_id),
                           headers = {"X-Client-Id": self.client_id},
                           timeout = 10)
        if req.status_code == 200:
            raw = req.json()
            res = raw['anime']
            res['episodes'] = raw['linked']['episodes']
            return res
        elif req.status_code == 404:
            print(req.text)
            raise self.AnimeNotFound
        else:
            raise requests.HTTPError("Not valid HTTP status code: {}".format(req.status_code), response = req)

    class AnimeNotFound(Exception):
        pass


class InvalidContentType(Exception):
    pass


class FileTooLarge(Exception):
    pass


def determine_filename(filename, mime):
    print(mime)
    filename = secure_filename(filename)
    ext = mimetypes.guess_extension(mime)
    if ext not in ['.jpg', '.png', '.gif', '.bmp', '.webp', '.jpeg']:
        raise InvalidContentType
    filename = "{}{}".format(filename, ext)
    return filename


def download_img_from_url(url, folder, filename):
    # Create a temp file to store the file
    tmpfile = tempfile.mkstemp()

    # Grab the file
    req = requests.get(url, stream = True)

    # Now we write to the tenp file in 2k chunk
    f = open(tmpfile[1], "wb")
    for chunk in req.iter_content(2048):
        f.write(chunk)
        if f.tell() > 1024 * 1024 * 10:  # If file is larger than 10 megabytes
            # Cleanup first
            f.close()
            os.unlink(tmpfile)
            raise FileTooLarge
    f.close()

    # Now we determine the extension based on the content type
    filename = determine_filename(filename, req.headers['Content-Type'])
    print(filename)
    # Things are ok, now we move the tempfile
    shutil.move(tmpfile[1], folder)
    return filename


hummingbird_api = HummingbirdAPI(config.HUMMINGBIRD_CLIENT_ID)


@need_to_login
def anime_import_hummingbird():
    class AnimeAddViaHummingbird(FlaskForm):
        season_id = IntegerField("Season ID", validators = [validators.DataRequired()])
        mal_id = IntegerField("MyAnimeList ID", validators = [validators.DataRequired()])

    form = AnimeAddViaHummingbird()
    if form.validate_on_submit():
        try:
            season = Season.get(Season.id == form.data['season_id'])
        except Season.DoesNotExist:
            return json.jsonify(result = "Invalid season id")

        # Grab the JSON info
        try:
            anime = hummingbird_api.get_anime(form.data['mal_id'], is_mal = True)
        except HummingbirdAPI.AnimeNotFound:
            return json.jsonify(result = "Anime not found")

        # Then we download the image
        # Everything should be fine before adding new entries to db
        try:
            poster_image = download_img_from_url(anime['poster_image'],
                                                 config.ANIME_POSTER_FOLDER,
                                                 "{}".format(form.data['mal_id']))
            cover_image = download_img_from_url(anime['cover_image'],
                                                config.ANIME_COVER_FOLDER,
                                                "{}".format(form.data['mal_id']))
        except InvalidContentType:
            return json.jsonify(result = "Invalid Content-Type received while download an image")
        except FileTooLarge:
            return json.jsonify(result = "An image is too large (the maximum size is 10MB")

        anime['poster_image'] = poster_image
        anime['cover_image'] = cover_image

        # It's best to be atomic in case anything wrong happens
        with database.atomic():
            # Create Anime entry
            anime_entry = Anime.create(anime_name = anime['titles']['romaji'],
                                       season = season,
                                       metadata = anime)

            # Then we create the episode
            for episode in anime_entry.metadata['episodes']:
                episode_entry = Episode.create(anime = anime_entry,
                                               episode_number = episode['id'],
                                               metadata = episode)

            # Then we add in the tags (or genres if you prefer it that way)
            for genre in anime_entry.metadata['genres']:
                tag, _ = Tag.get_or_create(tag_name = genre)
                _ = AnimeTagMap.create(tag_id = tag,
                                       anime_id = anime_entry)

            # All done
            return json.jsonify(result = "success", anime_id = anime_entry.id)

    else:
        return json.jsonify(result = "Invalid form data")


@need_to_login
def anime_page(id):
    pass


urlMapping = [
    ("/ajax/anime/import_hummingbird", ["POST"], anime_import_hummingbird),
    ("/admin/<int:id>", ["GET"], anime_page)
]
