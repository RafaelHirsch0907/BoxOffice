from flask import render_template, url_for, redirect
from bilheteria import app, dataBase, bcrypt
from flask_login import login_required, login_user, logout_user, current_user