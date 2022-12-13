from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import current_user
from sqlalchemy import JSON
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired

from .models.inventory import Inventory


from flask import Blueprint
bp = Blueprint('inventory', __name__)

@bp.route('/inventory', methods = ['GET','POST'])
def inventory():
    if current_user.is_authenticated:
        inventory = Inventory.get(current_user.id)
    return render_template('inventory.html',inventory = inventory)

class AddProductForm(FlaskForm):
    product_id = IntegerField('Product_id', validators=[DataRequired('Enter product ID')])
    quantity = IntegerField('Quantity', validators=[DataRequired('Enter quantity')])
    price = FloatField('Price', validators=[DataRequired('Enter Price')])
    product_description = StringField('Description', validators=[DataRequired('Enter description')])
    submit = SubmitField('Add')

@bp.route('/add_product', methods=['GET', 'POST'])
def add_product(): 
    form = AddProductForm()
    if form.validate_on_submit():
        if Inventory.add_product(form.product_id.data, form.quantity.data, form.price.data, form.product_description.data):
            return redirect(url_for('inventory.add_product'))
        flash("Product Added Successfully")
    return render_template('add_product.html',form = form)

class UpdateProductForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired('Enter quantity')])
    price = FloatField('Price', validators=[DataRequired('Enter Price')])
    product_description = StringField('Description', validators=[DataRequired('Enter description')])
    submit = SubmitField('Add')

@bp.route('/update_product/<seller_id>/<product_id>/', methods=['GET', 'POST'])
def update_product(seller_id, product_id):
    form = UpdateProductForm()
    if form.validate_on_submit():
        if Inventory.edit_product(product_id, form.quantity.data, form.price.data, form.product_description.data):
            return redirect(url_for('inventory.inventory'))
    return render_template('update_product.html',form = form)

@bp.route('/remove_product/<seller_id>/<product_id>/', methods=['GET', 'POST'])
def remove_product(seller_id, product_id):
    if Inventory.remove_product(product_id):
        flash('Congratulations, you have succefully removed the product!')
    return redirect(url_for('inventory.inventory'))