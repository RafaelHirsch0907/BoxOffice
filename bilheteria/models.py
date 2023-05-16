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
    regular = dataBase.Column(dataBase.String, nullable=False, default='R')
    vip = dataBase.Column(dataBase.String, nullable=False)
    notWhithdrawn = dataBase.Column(dataBase.Integer, default=0, nullable=False)
    tickets = dataBase.relationship("Ticket", backref="user", lazy=True)
    

class Ticket(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    #ticket = dataBase.Column(dataBase.String, default="default.png")
    status = dataBase.Column(dataBase.String, nullable=False, default='A')
    userId = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('user.id'), nullable=False)
    vip = dataBase.Column(dataBase.String, nullable=False)
    sales = dataBase.relationship("Sale", backref="sale", lazy=True)


class Sale(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    createDate = dataBase.Column(dataBase.DateTime, nullable=False, default=datetime.utcnow())
    ticketId = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('ticket.id'), nullable=False)
    delivery = dataBase.Column(dataBase.String, nullable=False)
    price = dataBase.Column(dataBase.Numeric, nullable=False)


class Show(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    name = dataBase.Column(dataBase.String, nullable=False)
    synopsis = dataBase.Column(dataBase.String, nullable=False)
    ticketsAvailable = dataBase.Column(dataBase.Integer, nullable=False, default=85)
    vipTicketsAvailable = dataBase.Column(dataBase.Integer, nullable=False, default=15)
    image = dataBase.Column(dataBase.String, default="default.png")