from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import Email, Length, EqualTo, DataRequired, email_validator, ValidationError
from app.models import User
from flask_login import current_user
from app.helpers import lookup
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
    validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', 
    validators=[DataRequired(), Email()])

    password = PasswordField('Password', 
    validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', 
    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign-Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different username")

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError("That email is taken. Please choose a different email")



class LoginForm(FlaskForm):
    email = StringField('Email', 
    validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')  


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
    validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', 
    validators=[DataRequired(), Email()])

    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg','jpeg', 'png', 'webp'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose a different username")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email = email.data).first()
            if email:
                raise ValidationError("That email is taken. Please choose a different email")


class QuoteForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired()])
    
    # price = TextAreaField('Price', validators=[DataRequired()])

    submit = SubmitField("Submit")

    # close = SubmitField("Close")
    # def validate_symbol(self, symbol):
    #     if lookup(symbol.data) == None or symbol.data is None:
    #         raise ValidationError("Enter correct symbol")


class BuyForm(FlaskForm):

    symbol = StringField('Symbol', validators=[DataRequired()])

    quantity = IntegerField('Quantity', validators=[DataRequired()])

    submit = SubmitField('Buy')


class SellForm(FlaskForm):

    symbol = StringField('Symbol', validators=[DataRequired()])

    quantity = IntegerField('Quantity', validators=[DataRequired()])

    submit = SubmitField('Sell')