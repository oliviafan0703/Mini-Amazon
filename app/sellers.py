from flask import render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from flask import Blueprint
from flask_login import current_user

from app.models.product import Product
from app.models.sellerP import SellerP
from app.models.seller import Seller
from app.models.orderP import OrderP
bp = Blueprint('Sellers', __name__)

@bp.route('/soldProducts/<seller_id>', methods=['GET', 'POST'])
def soldProducts(seller_id):
    products = SellerP.get_order_history(seller_id)
    
    processed_products = []
    for product in products:
        print(product.__dict__)
        processed_products.append(product.__dict__)

    
    for product in processed_products:
        overall_fulfillment = OrderP.is_order_fulfilled(product["order_id"])
        product['overall_fulfillment'] = overall_fulfillment

    created_products = SellerP.get_created_products(current_user.id)
    print(created_products)
    return render_template('seller.html', inventory_data=products, created_products = created_products)

class UpdateFulfillmentForm(FlaskForm):
    new_fulfillment = BooleanField('If fulfilled, check the box. If not, save without checking the box.')
    submit = SubmitField('Save')

@bp.route('/update_fulfillment/<seller_id>/<product_id>/<order_id>', methods=['GET', 'POST'])
def update_fulfillment(seller_id, product_id, order_id):
    form = UpdateFulfillmentForm()
    if form.validate_on_submit():
        if Seller.update_fulfillment(seller_id, product_id, order_id, form.new_fulfillment.data):
            return redirect(url_for('Sellers.soldProducts', seller_id = seller_id))
    return render_template('update_fulfillment.html', form = form)

# @bp.route('/createdProducts', methods=['GET', 'POST'])
# def createdProducts():
#     seller_id = current_user.id
#     products = SellerP.get_created_products(seller_id)
#     return render_template('seller.html', created_products=products)