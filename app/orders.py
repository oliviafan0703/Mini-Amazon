from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from flask import Blueprint

from app.models.orderP import OrderP
bp = Blueprint('Orders', __name__)


class OrdersForm(FlaskForm):
    id = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/Orders', methods=['GET', 'POST'])
def Orders():
    form = OrdersForm()
    targetID = form.id.data
    #orders = Order.get_orders(targetID)
    orders = OrderP.get_ordersP(targetID)
    print(orders)


    order_ids = OrderP.get_order_numbers_by_uid(current_user.id)
    print(current_user.id)
    print("order_ids")
    print(order_ids)
    order_data = {}
    for order in order_ids:
        if order in orders:
            continue
        order_data[order.order_id] = {'num_products' : order.num_products, 'fulfill_status' : order.num_fulfilled == order.num_products, 'time':order.timestamp.strftime('%m/%d/%Y'), 'total': round(order.total,2)}
    print(order_data)
    # order data has unique order id, followed by their timestamps. 
    return render_template('order.html', order_data=order_data, form=form)




