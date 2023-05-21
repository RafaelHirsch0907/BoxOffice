from bilheteria import dataBase, loginManager
from datetime import datetime
from flask_login import UserMixin

@loginManager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

class User(dataBase.Model, UserMixin):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    username = dataBase.Column(dataBase.String, nullable=False)
    email = dataBase.Column(dataBase.String, nullable=False, unique=True)
    password = dataBase.Column(dataBase.String, nullable=False)
    regular = dataBase.Column(dataBase.Boolean, nullable=False, default=True)
    vip = dataBase.Column(dataBase.Boolean, nullable=False)
    adm = dataBase.Column(dataBase.Boolean, nullable=False, default=False)
    notwhithdrawn = dataBase.Column(dataBase.Integer, default=0, nullable=False)
    tickets = dataBase.relationship("Ticket", backref="user", lazy=True)
    

class Ticket(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    #ticket = dataBase.Column(dataBase.String, default="default.png")
    status = dataBase.Column(dataBase.Boolean, nullable=False, default=True)
    userId = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('user.id'), nullable=False)
    showId = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('show.id'), nullable=False)
    vip = dataBase.Column(dataBase.Boolean, nullable=False, default=False)
    seatId = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('seat.id'), nullable=False)
    sales = dataBase.relationship("Sale", backref="sale", lazy=True)


class Sale(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    createDate = dataBase.Column(dataBase.DateTime, nullable=False, default=datetime.utcnow())
    ticketId = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('ticket.id'), nullable=False)
    delivery = dataBase.Column(dataBase.String, nullable=False)
    amountTickets = dataBase.Column(dataBase.Integer, nullable=False)
    price = dataBase.Column(dataBase.Numeric, nullable=False)


class Show(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    name = dataBase.Column(dataBase.String, nullable=False)
    synopsis = dataBase.Column(dataBase.String, nullable=False)
    ticketsAvailable = dataBase.Column(dataBase.Integer, nullable=False, default=90)
    vipTicketsAvailable = dataBase.Column(dataBase.Integer, nullable=False, default=10)
    coverImage = dataBase.Column(dataBase.String, default="default.png")
    date = dataBase.Column(dataBase.DateTime, nullable=False, unique=True)
    tickets = dataBase.relationship("Ticket", backref="show", lazy=True)

class Seat(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    row = dataBase.Column(dataBase.String, nullable=False)
    column = dataBase.Column(dataBase.Integer, nullable=False)
    seat = dataBase.Column(dataBase.String, nullable=False)
    available = dataBase.Column(dataBase.Boolean, default=True)
    tickets = dataBase.relationship("Ticket", backref="show", lazy=True)  