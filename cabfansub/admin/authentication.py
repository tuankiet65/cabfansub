from flask import render_template, request, redirect, session, json, url_for, g
from functools import wraps

from cabfansub import async
from cabfansub.common import timeSubtract, genRandomString
from cabfansub.database import User, LoginToken, IncorrectPassword, ForgotToken, database, create_all_tables


def need_to_login(func):
    @wraps(func)
    def tmp_func(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("admin.login_page"))
        return func(*args, **kwargs)

    return tmp_func


def login_page():
    return render_template("admin/authentication/login.html")


def login():
    username = request.form['username']
    password = request.form['password']
    try:
        user = User.get(User.username == username)
    except User.DoesNotExist:
        return json.jsonify({"result": "failure"})
    try:
        session['tokenKey'], session['tokenValue'] = user.login(password)
    except (User.DoesNotExist, LoginToken.DoesNotExist, IncorrectPassword):
        return json.jsonify({"result": "failure"})
    if 'remember-me' in request.form:
        session.permanent = True
    return json.jsonify({"result": "success"})


def sign_out():
    User.logout()
    return redirect(url_for("admin.login_page"))


def register_page():
    return render_template("admin/authentication/register.html")


def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    realname = request.form['realname']
    User.create(username = username, password = password, email = email, real_name = realname)
    return redirect("/login?created")


def forgot_page():
    return render_template("admin/authentication/forgot.html")


def reset_password():
    email = request.form['email']
    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        return json.jsonify(result = "not found")
    ft_obj = ForgotToken.new(user_id = user.id)
    mail_content = render_template("authentication/forgotEmail.html",
                                   token = ft_obj.token,
                                   expiration = ft_obj.timestamp.isoformat())
    async.sendMail(email, "Reset your password | Cab Fansub", mail_content)
    return json.jsonify(result = "success")


def reset_password2():
    if 'token' not in request.args:
        return redirect("/")
    token = request.args['token']
    with database.atomic():
        try:
            token_obj = ForgotToken.get(
                (ForgotToken.token == token) & (ForgotToken.timestamp >= timeSubtract(days = 1)))
        except ForgotToken.DoesNotExist:
            return redirect("/login?invalidToken")
        user = token_obj.user_id
        user.password = genRandomString(20)
        user.save()
        token_obj.delete_instance()
    mail_content = render_template("authentication/forgot2Email.html",
                                   newPassword = user.password)
    async.sendMail(user.email, "New password | Cab Fansub", mail_content)
    return redirect("/login?resetSuccess")


urlMapping = [
    ("/login", ["GET"], login_page),
    ("/login", ["POST"], login),
    ("/forgot", ["GET"], forgot_page),
    ("/forgot", ["POST"], reset_password),
    ("/forgot2", ["GET"], reset_password2),
    ("/signout", ["GET"], sign_out),
    ("/register", ["GET"], register_page),
    ("/register", ["POST"], register),
]
