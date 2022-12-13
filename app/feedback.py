from flask import jsonify, render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
import json
from sqlalchemy import JSON
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.models.product import Product

from flask import Blueprint
bp = Blueprint('feedback', __name__)

class FeedbackForm(FlaskForm):
    id = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Save ID')

# @bp.route('/cart_add', methods=['GET', 'POST'])
# def cart_add():
#     print("current user:")
#     print(current_user.id)
#     if request.method == "POST":
#         print(request.data)
#         objectToAdd = json.loads(request.data)
#     print(objectToAdd)

#     #success code
#     return "", 201
        

@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    targetID = form.id.data
    products = Product.get_user_cart(current_user.id)
    print(products)
    print("opened this page")
    return render_template('feedback.html', form=form)

@bp.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    form = FeedbackForm()
    targetID = form.id.data
    products = Product.get_user_cart(targetID)
    if len(products) > 0:
        flash("Congratulations, you successfully ")
    else:
        flash("Sorry, No Item in Cart!!")    
    return redirect(url_for('feedback.feedback'))
