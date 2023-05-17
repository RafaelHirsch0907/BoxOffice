from flask import render_template, url_for, redirect
from bilheteria import app, dataBase, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from bilheteria.forms import FormShow, FormCreateShow, FormLogin, FormCreateLogin
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

@app.route("/createlogin", methods=["GET", "POST"])
def createlogin():
    formCreateLogin = FormCreateLogin()
    if formCreateLogin.validate_on_submit():
        password = bcrypt.generate_password_hash(formCreateLogin.password.data)
        user = User(username=formCreateLogin.username.data, password=password, email=formCreateLogin.email.data, regular=True, vip=formCreateLogin.vip.data, adm=False, notwhithdrawn=0)

        dataBase.session.add(user)
        dataBase.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("profile", user_id=user.id))
    return render_template("createlogin.html", form=formCreateLogin)

@app.route("/createshow", methods=["GET", "POST"])
@login_required
def createshow():
    formCreateShow = FormCreateShow()
    if formCreateShow.validate_on_submit():
        show = Show(name=formCreateShow.name.data, password=password, email=formCreateShow.email.data, regular=True, vip=formCreateShow.vip.data, adm=False, notwhithdrawn=0)

        dataBase.session.add(user)
        dataBase.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("profile", user_id=user.id))
    return render_template("createlogin.html", form=formCreateShow)