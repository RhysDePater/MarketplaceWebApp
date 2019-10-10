
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, TextAreaField, SubmitField, StringField, PasswordField, IntegerField, FileField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired


# creates the login information
class LoginForm(FlaskForm):
    name = StringField("User Name", validators=[
        InputRequired('Enter user name')])
    password_hash = PasswordField("Password", validators=[
        InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form


class RegisterForm(FlaskForm):
    name = StringField("User Name", validators=[
                       InputRequired('Enter a Name')])
    emailid = StringField('Email Address', validators=[
                          InputRequired('Enter an Email'), Email()])

    phone = IntegerField('Phone Number', validators=[
                         InputRequired('Please enter a Phone Number'), NumberRange(min=100000000, max=9999999999, message="Please enter a valid 10 digit long phone number")])

    location = StringField("Address", validators=[
                           InputRequired('Please enter an address')])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired('Please enter a password'),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")


ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}


class CreationForm(FlaskForm):
    name = StringField("Item Title", validators=[
                       InputRequired('Enter a Name')])
    model = StringField("Item model", validators=[
        InputRequired('Enter a model name')])
    price = FloatField('Price', validators=[
        InputRequired('Please enter valid Price')])
    category = SelectField("Category", choices=[(
        '1', 'CPU'), ('2', 'GPU'), ('3', 'CASE'), ('4', 'Peripherals'), ('5', 'Power Supply')])
    description = TextAreaField("Description", validators=[
        InputRequired('Enter a Name')])
    quality = SelectField("Quality", choices=[(
        '1', 'New'), ('2', 'Used/Excelent'), ('3', 'Used/Good'), ('4', 'Used/Moderate'), ('5', 'Used/Needs Repairs')])
    image = FileField("Product Image:", validators=[FileRequired(message='Image can not be empty'),
                                                    FileAllowed(ALLOWED_FILE, message='Only support png, jpg, JPG, PNG, bmp')])
    submit = SubmitField("Post Item")
