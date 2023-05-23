from flask import render_template, url_for, redirect
from bilheteria import app, dataBase, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from bilheteria.forms import FormCreateShow, FormLogin, FormCreateLogin
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
        password = bcrypt.generate_password_hash(formCreateLogin.password.data).decode('utf-8')
        user = User(username=formCreateLogin.username.data, password=password, email=formCreateLogin.email.data, regular=True, vip=formCreateLogin.vip.data, adm=False, notwhithdrawn=0)
        dataBase.session.add(user)
        dataBase.session.commit()
        
        login_user(user, remember=True)
        return redirect(url_for("profile", user_id=user.id))
    #else:
    #   return redirect(url_for("createlogin", message="Email ou senha incorretos, tente novamente"))
    return render_template("createlogin.html", form=formCreateLogin)

@app.route("/profile/<user_id>", methods=["GET", "POST"])
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        return render_template("profile.html", user=current_user, form=None)
    else:
        return render_template("profile.html", user=current_user, form=None, message="Acesso negado. Você não pode acessar o perfil de outro usuário")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/createshow", methods=["GET", "POST"])
@login_required
def createshow():
    formCreateShow = FormCreateShow()
    if not current_user.adm:
        return render_template("shows.html", message="Acesso negado. Somente administradores podem acessar esta página.")
    else:
        if formCreateShow.validate_on_submit():
            archive = formCreateShow.coverImage.data
            securityName = secure_filename(archive.filename)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], securityName)
            archive.save(path)
            show = Show(name=formCreateShow.name.data, synopsis=formCreateShow.synopsis.data, coverImage=securityName, date=formCreateShow.date.data, ticketsAvailable=85, vipTicketsAvailable=15)
            dataBase.session.add(show)
            dataBase.session.commit()
            return redirect(url_for("shows"))
    return render_template("createshow.html", form=formCreateShow)

@app.route("/shows")
def shows():
    shows = Show.query.order_by(Show.name.desc()).all()
    return render_template("shows.html", shows=shows)

#@app.route("/show/<show_id>")
#def show(show_id):

#    return render_template("show.html", show=show)