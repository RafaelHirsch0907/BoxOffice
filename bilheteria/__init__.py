from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:3qlKBAgZckJF2SNQ188Y@containers-us-west-177.railway.app:6538/railway"
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "ae926c34f7402981c94adedbc9f8a477"
app.config["UPLOAD_FOLDER"] = "static/photos_theater"

dataBase = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = "homepage"

from bilheteria import routes