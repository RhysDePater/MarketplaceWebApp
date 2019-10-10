from flask import Blueprint, render_template, session
from flask_login import login_required
from .models import Item, Purchased_item, Bid
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    items = Item.query.filter_by(purchased=None).all()

    return render_template('index.html', items=items, heading='Items For Sale')


@bp.route('/selling')
@login_required
def selling():
    items = Item.query.filter_by(
        user_id=session['user_id'], purchased=None).all()

    return render_template('index.html', items=items, heading="Items You Have For Sale")


@bp.route('/sold')
@login_required
def sold():
    items = Item.query.filter(
        Item.user_id == session['user_id'], Item.purchased != None).all()

    return render_template('index.html', items=items, heading="Items You Have Sold")


@bp.route('/bid')
@login_required
def bid():
    items = Item.query.filter(Item.bids != None, Item.purchased == None).all()
    bids = Bid.query.all()

    return render_template('bid.html', items=items, bids=bids, heading="Items You Have Bidded On")


@bp.route('/purchases')
@login_required
def purchases():
    items = Item.query.filter(Item.purchased != None).all()
    purchases = Purchased_item.query.all()

    return render_template('purchases.html', items=items, purchases=purchases, heading="Items You Have Purchased")
