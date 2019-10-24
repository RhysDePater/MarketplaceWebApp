from flask import (
    Blueprint, flash, render_template, request, url_for, redirect, session
)
from .models import Item, User, Bid, Purchased_item
from .forms import CreationForm, EditForm, bidForm
from . import db
from flask_login import current_user
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
import os
from flask_login import login_required

# shaun updated-30/9/2019 OPEN
bp = Blueprint('item', __name__)


@bp.route('/viewItem/<id>', methods=['POST', 'GET'])
def show(id):
    bid = bidForm()
    users = User.query.all()
    item = Item.query.filter_by(id=id).first()
    if(current_user.is_authenticated):
        bids = Bid.query.filter_by(user_id=current_user.id, item_id=id).first()
    else:
        bids = None
    if bid.validate_on_submit():
        bidder = User.query.filter_by(id=current_user.id).first()
        newBid = Bid(bidder_name=bidder.name, bidder_email=bidder.emailid,
                     bidder_phone=bidder.phone_no, user_id=bidder.id, item_id=id)
        db.session.add(newBid)
        db.session.commit()
        message = "Bid Placed Successfully!"

        # refresh the data pulled from the database so they can't spam the button
        bid = bidForm()
        users = User.query.all()
        item = Item.query.filter_by(id=id).first()
        bids = Bid.query.filter_by(user_id=current_user.id, item_id=id).first()

        return render_template('itemDetails.html', item=item, bid=bid, message=message, bids=bids, users=users)
    return render_template('itemDetails.html', item=item, bid=bid, bids=bids, users=users)


@bp.route('/sellItem/<id>', methods=['POST', 'GET'])
def sellItem(id):
    bid = Bid.query.filter_by(id=id).first()
    item = Item.query.filter_by(id=bid.item_id).first()

    newPurchase = Purchased_item(buyer=bid.bidder_name, seller=item.seller,
                                 created_date=item.created_date, item_id=bid.item_id, seller_id=item.user_id, bid_id=bid.id)
    db.session.add(newPurchase)
    db.session.commit()
    return redirect('/soldItem/' + str(item.id))


@bp.route('/soldItem/<id>', methods=['GET', 'POST'])
@login_required
def soldItem(id):
    bid = Bid.query.filter_by(item_id=id).first()
    item = Item.query.filter_by(id=id).first()
    purchase = Purchased_item.query.filter_by(bid_id=bid.id).first()
    users = User.query.all()

    return render_template('soldItemDetails.html', item=item, users=users, purchase=purchase, bid=bid)


@bp.route('/manageItem/<id>', methods=['POST', 'GET'])
@login_required
def manage(id):

    users = User.query.all()
    item = Item.query.filter_by(id=id).first()
    bids = Bid.query.all()

    # form.name.name = Item['name']
    # form.model.data = Item['model']
    if request.method == 'GET':
        form = EditForm(formdata=MultiDict(
            {'name': item.name, 'price': item.price, 'category': item.category, 'model': item.model, 'description': item.description, 'quality': item.quality, 'image': item.image}))
    else:
        form = EditForm()
    if request.method == 'POST' and form.validate():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.model = form.model.data
        item.description = form.description.data
        item.quality = form.quality.data
        try:
            item.image = checkUploadFile(form)
        except:
            item.image = item.image
        db.session.commit()
        return render_template('itemManage.html', form=form, item=item, users=users, bids=bids)
    return render_template('itemManage.html', form=form, item=item, users=users, bids=bids)


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
