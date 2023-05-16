from bilheteria import dataBase, app
from bilheteria.models import User, Sale, Ticket, Show

with app.app_context():
    dataBase.create_all()