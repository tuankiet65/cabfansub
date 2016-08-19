from flask import Blueprint, session, g, redirect, url_for, render_template
from cabfansub.database import User, LoginToken, InvalidToken, create_all_tables

from cabfansub.admin.authentication import urlMapping as authUrlMapping, need_to_login
from cabfansub.admin.ajax import urlMapping as ajaxUrlMapping
from cabfansub.admin.seasons import urlMapping as seasonsUrlMapping
from cabfansub.admin.anime import urlMapping as animeUrlMapping

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


urlMapping = authUrlMapping
urlMapping.extend(ajaxUrlMapping)
urlMapping.extend(seasonsUrlMapping)
urlMapping.extend(animeUrlMapping)
for urlMap in urlMapping:
    admin.add_url_rule(urlMap[0], view_func = urlMap[2], methods = urlMap[1])


@admin.route("/")
@need_to_login
def index():
    return redirect(url_for("admin.dashboard"))


@admin.route("/dashboard")
@need_to_login
def dashboard():
    return render_template("admin/dashboard.html")
