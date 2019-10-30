from flask import Blueprint, render_template, session
from flask_login import login_required
from .models import Item, Purchased_item, Bid
from . import db
from .forms import searchForm
from sqlalchemy import desc

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    formSearch = searchForm()
    if formSearch.validate_on_submit():
        print('Search')
        cate = formSearch.category.data

        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    items = Item.query.filter_by(
        purchased=None).order_by(desc(Item.id)).all()

    return render_template('index.html', type="view", items=items, formSearch=formSearch, heading='Items For Sale')


@bp.route('/selling', methods=['GET', 'POST'])
@login_required
def selling():
    formSearch = searchForm()
    if formSearch.validate_on_submit():
        print('Search')
        cate = formSearch.category.data

        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    items = Item.query.filter_by(
        user_id=session['user_id'], purchased=None).order_by(desc(Item.id)).all()

    return render_template('items.html', type="selling", items=items, formSearch=formSearch, heading="Items You Have For Sale")


@bp.route('/sold', methods=['GET', 'POST'])
@login_required
def sold():
    formSearch = searchForm()
    if formSearch.validate_on_submit():
        print('Search')
        cate = formSearch.category.data

        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    items = Item.query.filter(
        Item.user_id == session['user_id'], Item.purchased != None).order_by(desc(Item.id)).all()

    return render_template('items.html', type="sold", items=items, formSearch=formSearch, heading="Items You Have Sold")


@bp.route('/bid', methods=['GET', 'POST'])
@login_required
def bid():
    formSearch = searchForm()
    if formSearch.validate_on_submit():
        print('Search')
        cate = formSearch.category.data

        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    items = Item.query.filter(Item.bids != None, Item.purchased == None).order_by(
        desc(Item.id)).all()
    bids = Bid.query.all()

    return render_template('bid.html', items=items, formSearch=formSearch, bids=bids, heading="Items You Have Bidded On")


@bp.route('/purchases', methods=['GET', 'POST'])
@login_required
def purchases():
    formSearch = searchForm()
    if formSearch.validate_on_submit():
        print('Search')
        cate = formSearch.category.data

        items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
            desc(Item.id)).all()
        return render_template('items.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale - ' + cate)

    items = Item.query.filter(Item.purchased != None).order_by(
        desc(Item.id)).all()
    purchases = Purchased_item.query.all()

    return render_template('purchases.html', items=items, formSearch=formSearch, purchases=purchases, heading="Items You Have Purchased")


# @bp.route('/viewItem', methods=['GET', 'POST'])
# @login_required
# def viewItem():
#     formSearch = searchForm()
#     if formSearch.validate_on_submit():
#         print('Search')
#         cate = formSearch.category.data

#         items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
#             desc(Item.created_date)).all()
#         return render_template('index.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale')

#     items = Item.query.filter_by(purchased=None).order_by(
#         desc(Item.created_date)).all()

#     return render_template('index.html', items=items, formSearch=formSearch, heading='Items For Sale')


# @bp.route('/manageItem', methods=['GET', 'POST'])
# @login_required
# def manageItem():
#     formSearch = searchForm()
#     if formSearch.validate_on_submit():
#         print('Search')
#         cate = formSearch.category.data

#         items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
#             desc(Item.created_date)).all()
#         return render_template('index.html', type="view", items=items1, formSearch=formSearch, heading='Items For Sale')

#     items = Item.query.filter_by(purchased=None).order_by(
#         desc(Item.created_date)).all()

#     return render_template('index.html', type="view", items=items, formSearch=formSearch, heading='Items For Sale')


# @bp.route('/soldItem', methods=['GET', 'POST'])
# @login_required
# def soldItem():
#     formSearch = searchForm()
#     if formSearch.validate_on_submit():
#         print('Search')
#         cate = formSearch.category.data

#         items1 = Item.query.filter_by(purchased=None, category=cate).order_by(
#             desc(Item.created_date)).all()
#         return render_template('index.html',  type="view", items=items1, formSearch=formSearch, heading='Items For Sale')

#     items = Item.query.filter_by(purchased=None).order_by(
#         desc(Item.created_date)).all()

#     return render_template('index.html', type="view", items=items, formSearch=formSearch, heading='Items For Sale')
