from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TimeField, FloatField
from wtforms.validators import InputRequired, EqualTo
from wtforms.widgets import TextArea, DateTimeInput


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


class NewAuctionForm(FlaskForm):
    auction_end = DateField('Auction end', id='inputAuctionEnd', validators=[InputRequired(message='Date is required')])
    auction_end_time = TimeField(validators=[InputRequired(message='Time is required')])
    price = FloatField('Start price', id='inputStartPrice', default=0, validators=[InputRequired(message='Start price is required')])
    name = StringField('Name', id='inputName', validators=[InputRequired(message='Name is required')])
    description = StringField('Description', id='inputDescription', widget=TextArea(), validators=[InputRequired(message='Description is required')])
    img_link = StringField('Image link', id='inputImgLink', validators=[InputRequired(message='Link is required')])
