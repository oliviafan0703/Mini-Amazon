from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from datetime import datetime

from .models.user import User
from .models.review import Review
from .models.product import Product
from .models.orderP import OrderP


from flask import Blueprint
bp = Blueprint('public_view', __name__)

@bp.route('/profile/<uid>', methods=['GET', 'POST'])
def public_view(uid):
    print(uid)
    profile_user = User.get(uid)
    is_seller = User.is_seller(uid)
    seller_addr = User.get_address(uid) 
    seller_items = Product.get_seller_inventory_2(uid)
    reviews = Review.get_seller_reviews(uid)
    print(reviews)
    print(profile_user)
    return render_template("public_profile.html", is_seller=is_seller, profile_user=profile_user,
                            seller_addr=seller_addr, reviews=reviews, seller_items=seller_items)

class ReviewFormS(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Add')

@bp.route('/profile/<uid>/review', methods=['GET', 'POST'])
def public_view_review(uid):
    form = ReviewFormS()
    seller = User.get(uid)
    time_post = datetime.now()
    user_id = current_user.id

    ordered_seller = OrderP.check_ordered_seller(uid, user_id)
    if not ordered_seller:
        flash('You have not order product from this seller before.')
        return redirect(url_for('public_view.public_view', uid = uid))

    submitted_review_seller = Review.check_submitted_review_seller(uid, user_id)
    if submitted_review_seller:
        flash('You cannot submit multiple review for the same seller.')
        return redirect(url_for('public_view.public_view', uid = uid))

    if form.validate_on_submit():
        if Review.add_review_seller(uid, 
                            form.rating.data,
                            form.title.data,
                            form.content.data,
                            time_post):
                            print("successsssss!")
                            flash("Successfully added review!")
    return render_template("add_review_seller.html", form=form, seller_id=uid, seller=seller)

