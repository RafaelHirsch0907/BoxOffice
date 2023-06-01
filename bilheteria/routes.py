from flask import render_template, url_for, redirect, flash
from bilheteria import app, dataBase, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from bilheteria.forms import (
    FormCreateShow,
    FormLogin,
    FormCreateLogin,
    FormCreateTicket,
)
from bilheteria.models import User, Show, Ticket, Seat
from werkzeug.utils import secure_filename
from sqlalchemy import func
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
        password = bcrypt.generate_password_hash(formCreateLogin.password.data).decode(
            "utf-8"
        )

        max_id = dataBase.session.query(func.max(User.id)).scalar()
        if max_id is None:
            new_id = 1
        else:
            new_id = max_id + 1

        user = User(
            id=new_id,
            username=formCreateLogin.username.data,
            password=password,
            email=formCreateLogin.email.data,
            regular=True,
            vip=formCreateLogin.vip.data,
            adm=False,
            notwhithdrawn=0,
        )

        dataBase.session.add(user)
        dataBase.session.commit()

        login_user(user, remember=True)
        return redirect(url_for("profile", user_id=user.id))

    return render_template("createlogin.html", form=formCreateLogin)


@app.route("/profile/<user_id>", methods=["GET", "POST"])
@login_required
def profile(user_id):
    if int(user_id) == int(current_user.id):
        tickets = Ticket.query.filter_by(userId=current_user.id).all()
        for ticket in tickets:
            seat = Seat.query.filter_by(id=ticket.seatId).first()
            if seat:
                ticket.seat = seat
                ticket.seat_name = seat.seat
            else:
                ticket.seat_name = 'Seat não encontrado'
        return render_template("profile.html", user=current_user, tickets=tickets)
    else:
        return render_template(
            "profile.html",
            user=current_user,
            form=None,
            message="Acesso negado. Você não pode acessar o perfil de outro usuário",
        )


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
        return render_template(
            "shows.html",
            message="Acesso negado. Somente administradores podem acessar esta página.",
        )
    else:
        if formCreateShow.validate_on_submit():
            archive = formCreateShow.coverImage.data
            securityName = secure_filename(archive.filename)
            path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                securityName,
            )
            archive.save(path)

            max_id = dataBase.session.query(func.max(Show.id)).scalar()
            if max_id is None:
                new_id = 1
            else:
                new_id = max_id + 1

            show = Show(
                id=new_id,
                name=formCreateShow.name.data,
                synopsis=formCreateShow.synopsis.data,
                coverImage=securityName,
                date=formCreateShow.date.data,
                ticketsAvailable=85,
                vipTicketsAvailable=15,
            )

            dataBase.session.add(show)
            dataBase.session.commit()

            return redirect(url_for("shows"))
    return render_template("createshow.html", form=formCreateShow)


@app.route("/shows")
def shows():
    shows = Show.query.order_by(Show.name.desc()).all()
    return render_template("shows.html", shows=shows)


@app.route("/show/<show_id>", methods=["GET", "POST"])
@login_required
def show(show_id):
    if not current_user.regular:
        flash("Acesso negado. Somente usuários regulares podem acessar esta página.")
        return redirect(url_for("shows"))

    show = Show.query.get(show_id)
    form_create_ticket = None

    if show:
        form_create_ticket = FormCreateTicket(show_id=show_id)

        if form_create_ticket.validate_on_submit():
            max_id = Ticket.query.with_entities(func.max(Ticket.id)).scalar()
            new_id = (max_id or 0) + 1

            if current_user.vip:
                if form_create_ticket.vip.data:
                    price = 0
                else:
                    price = 50
            else:
                if form_create_ticket.delivery.data:
                    price = 65
                else:
                    price = 50

            ticket = Ticket(
                id=new_id,
                status=True,
                userId=current_user.id,
                showId=show_id,
                vip=form_create_ticket.vip.data,
                delivery=form_create_ticket.delivery.data,
                seatId=int(form_create_ticket.seatId.data),
                price=price,
                withdrawn=False
            )

            dataBase.session.add(ticket)
            dataBase.session.commit()
            return redirect(url_for("shows"))

        return render_template(
            "show.html", show=show, user=current_user, form=form_create_ticket
        )

    else:
        flash("Espetáculo não encontrado")
        return redirect(url_for("shows"))

@app.route("/withdraw_ticket/<ticket_id>", methods=["POST"])
@login_required
def withdraw_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    
    if ticket:
        ticket.withdrawn = True
        dataBase.session.commit()
        flash("Ingresso retirado com sucesso.")
    else:
        flash("Falha ao retirar o ingresso. Ingresso não encontrado.")
    
    return redirect(url_for("profile", user_id=current_user.id))