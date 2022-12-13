from functools import reduce
from flask import render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_login import UserMixin, current_user
from datetime import datetime
from flask import Blueprint

#plot imports
import pandas as pd
import json
import plotly
import plotly.express as px

from app.models.order import Order
from app.models.orderP import OrderP
from app.models.product import Product
from app.models.review import Review    

bp = Blueprint('Order_Details', __name__)

@bp.route('/orders/<order_id>', methods=['GET', 'POST'])
def order_details(order_id):
    print(order_id)
    #orders = Order.get_orders(targetID)
    # orders = OrderP.get_ordersP(targetID)
    # print(orders)

    orders = OrderP.get_orders_by_order_id(order_id)
    for order in orders:
        print(order.order_id)
    print(order.sellername)
    # print(orders.lastname)
    return render_template('order_details.html' ,order_data = orders)

# @bp.route('/plot', methods=['GET', 'POST'])
# def plot():
#     product_id = request.args['product_id']
#     order_ids = OrderP.get_order_sold_by_seller(product_id)

#     sales_history =[]
#     for order in order_ids:
#         sales_hist=[str(order.seller_id), order.total_quantity]
#         print(sales_hist)
#         sales_history.append(sales_hist)
#         # order_data[order.seller_id] = {'seller_id' : order.seller_id, 'total_quantity' : order.total_quantity}
#         # print(order_data)
        
#    # Students data available in a list of list
#     # students = [['Akash', 34],
#     #             ['Rithika', 30],
#     #             ['Priya', 31],
#     #             ['Sandy', 32],
#     #             ['Praneeth', 16],
#     #             ['Praveen', 17]]
     
#     # Convert list to dataframe and assign column values
#     df = pd.DataFrame(sales_history,
#                       columns=['Sellers', 'Sales'])
     
#     # Create Bar chart
#     fig = px.bar(df, x='Sellers', y='Sales', barmode='group')
     
#     # Create graphJSON
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
#     # Use render_template to pass graphJSON to html
#     return render_template('charts.html', graphJSON=graphJSON)
