from flask import Flask, render_template
from flask_wtf.csrf import CsrfProtect
from flask_babel import Babel

from .config import Config
from .admin import admin

app = Flask(__name__)
app.register_blueprint(admin)
config = Config()
app.config.from_object(config)
babel = Babel(app)
CsrfProtect(app)

@app.route("/")
def index():
    return render_template("index.html")
