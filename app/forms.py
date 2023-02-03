from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, EqualTo
from wtforms.widgets import NumberInput

from wtforms.widgets import TextArea


class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.')], id='inputEmail')
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')],
                             id='inputPassword')
    confirm_password = PasswordField('Confirm password',
                                     validators=[InputRequired(message='Password field is required.'),
                                                 EqualTo('password')], id='inputPasswordConfirm')
    submit = SubmitField('Register', id='submitButton')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.')], id='inputEmail')
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')],
                             id='inputPassword')
    submit = SubmitField('Log in', id='submitButton')


class BiddingForm(FlaskForm):
    price = IntegerField('Price from', widget=NumberInput(min=0, step=1), render_kw={"placeholder": "PLN"})
    submit = SubmitField('Bidding', id='biddingButton')


class NewAuctionForm(FlaskForm):
    auction_end = DateTimeField('Auction end', id='inputAuctionEnd')
    name = StringField('Name', id='inputName')
    description = StringField('Description', id='inputDescription', widget=TextArea())
    img_link = StringField('Image link', id='inputImgLink')
