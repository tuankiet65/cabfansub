from flask import Blueprint, session, g, redirect, url_for, render_template
from cabfansub.admin.authentication import urlMapping as authUrlMapping
from cabfansub.admin.ajax import urlMapping as ajaxUrlMapping
from cabfansub.database import User, LoginToken, InvalidToken, Season
from functools import wraps
admin = Blueprint("admin", __name__, url_prefix = "/admin")


@admin.before_request
def load_user_info():
    if ('tokenKey' not in session) or ('tokenValue' not in session):
        g.user = None
    else:
        try:
            g.user = LoginToken.use(session['tokenKey'], session['tokenValue'])
        except InvalidToken:
            User.logout()
            g.user = None


def need_to_login(func):
    @wraps(func)
    def tmp_func():
        if g.user is None:
            return redirect(url_for("admin.login"))
        return func

    return tmp_func

urlMapping = authUrlMapping
urlMapping.extend(ajaxUrlMapping)
for urlMap in urlMapping:
    admin.add_url_rule(urlMap[0], view_func = urlMap[2], methods = urlMap[1])


@need_to_login
@admin.route("/")
def index():
    return redirect(url_for("admin.dashboard"))

@need_to_login
@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")


@need_to_login
@admin.route("/seasons")
def seasons():
    seasons = Season.select()
    return render_template("admin/seasons.html", seasons = seasons)

@need_to_login
@admin.route("/season/<int:id>")
def season_list_anime(id):
    return render_template("admin/season_list_anime.html")