from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from .models import User
from .forms import LoginForm, RegisterForm
from . import db
from flask_login import login_user, logout_user

# for password storage
from werkzeug.security import generate_password_hash, check_password_hash

# create a blueprint
bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if(form.validate_on_submit()):
        user_name = form.name.data
        password = form.password_hash.data
        u1 = User.query.filter_by(name=user_name).first()

        # if there is no user with that name
        if u1 is None:
            error = 'Incorrect user name'
        # check the password - notice password hash function
        # takes the hash and password
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect password'
        if error is None:
            # all good, set the login_user
            login_user(u1, force=True)
            return redirect(url_for('main.index'))
        else:
            print(error)
            flash(error)
        # it comes here when it is a get method
    return render_template('user.html', form=form, heading='Login')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        print('Register form submitted')

        # get username, password and email from the form
        uname = form.name.data
        pwd = form.password.data
        email = form.emailid.data
        phone = form.phone.data
        address = form.location.data
        # don't store the password - create password hash
        pwd_hash = generate_password_hash(pwd)

        u1 = User.query.filter_by(name=uname).first()
        e1 = User.query.filter_by(emailid=email).first()

        if u1 != None:
            error = 'Username ' + uname + ' is taken, please choose another username.'
        elif e1 != None:
            error = 'Email ' + email + ' has already been used.'
        if error is None:
            new_user = User(name=uname, emailid=email, phone_no=phone,
                            password_hash=pwd_hash, location=address)
            db.session.add(new_user)
            db.session.commit()
            # commit to the database and redirect to HTML page
            return redirect(url_for('auth.login'))
        else:
            print(error)
            flash(error)

    return render_template('user.html', form=form, heading='Register')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
