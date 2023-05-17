from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:c3925dbaay@localhost/flasksql"
app.config["SECRET_KEY"] = "0a195e1fefcca8d874d9551596dab099"
app.config["UPLOAD_FOLDER"] = "static/photos_theater"

dataBase = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = "homepage"

from bilheteria import routes