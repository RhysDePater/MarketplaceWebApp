from flask import (
    Blueprint, flash, render_template, request, url_for, redirect, session
)
from .models import Item
from .forms import CreationForm
from . import db
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
from flask_login import login_required

# shaun updated-30/9/2019 OPEN
bp = Blueprint('item', __name__)


@bp.route('/creation', methods=['POST', 'GET'])
@login_required
def create():
    form = CreationForm()
    error = None
    if form.validate_on_submit():
        print('Register form submitted')

        # where i represents item
        iuser_name = current_user.name
        iname = form.name.data
        iprice = form.price.data
        icategory = form.category.data
        imodel = form.model.data
        idescription = form.description.data
        iquality = form.quality.data
        iImage = checkUploadFile(form)
        iUser_id = session["user_id"]
        # create a new user model object
        new_item = Item(seller=iuser_name, name=iname, price=iprice, category=icategory,
                        model=imodel, description=idescription, quality=iquality, image=iImage, user_id=iUser_id)
        db.session.add(new_item)
        db.session.commit()
        # commit to the database and redirect to HTML page
        return redirect(url_for('main.index'))

    return render_template('creation.html', form=form, heading='Item Creation')
# shaun updated-30/9/2019 CLOSE


def checkUploadFile(form):
    fp = form.image.data
    filename = fp.filename
    Base_Path = os.path.dirname(__file__)
    upload_path = os.path.join(
        Base_Path, 'static/images', secure_filename(filename))
    db_upload_path = 'static/images/'+secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path
