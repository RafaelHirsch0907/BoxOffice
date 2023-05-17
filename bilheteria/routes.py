from flask import render_template, url_for, redirect
from bilheteria import app, dataBase, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from bilheteria.forms import FormShow, FormCreateLogin, FormLogin
from bilheteria.models import User, Show
from werkzeug.utils import secure_filename
import os

@app.route("/", methods=["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        user = User.query.filter_by(email=formLogin.email.data).first()
        if user and bcrypt.check_password_hash(user.password, formLogin.password.data):
            login_user(user)
            return redirect(url_for("profile", user_id=user.id))
    return render_template("homepage.html", form=formLogin)