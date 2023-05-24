from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from bilheteria.models import User, Show

class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submitButton = SubmitField("Submit")

class FormCreateLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6,25)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    vip = BooleanField("VIP")
    submitButton = SubmitField("Create Login")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            return ValidationError("Email already registered, login to continue")
        
class FormCreateShow(FlaskForm):
    coverImage = FileField("Cover Image", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    synopsis = StringField("Synopsis", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    submitButton = SubmitField("Upload Show")

class FormCreateTicket(FlaskForm):
    vip = BooleanField("VIP")

#class FormCreateSale(FlaskForm):
