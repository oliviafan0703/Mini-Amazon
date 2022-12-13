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
bp = Blueprint('Product_Details', __name__)



@bp.route('/products/<product_id>', methods=['GET', 'POST'])
def Product_Details(product_id):
    print(product_id)
    product = Product.get(product_id)
    print(product)
    print(product.product_id)
    # vendors = Product.get_sellers_by_product(product.product_id)
    vendors = Product.get_sellers_by_product(product.product_id)
    print(vendors)

    reviews = Product.get_reviews_by_product(product.product_id)

    print(reviews)
    subtotal_rating = 0
    count5 = 0
    count4 = 0
    count3 = 0
    count2 = 0
    count1 = 0
    length = 0
    average_rating = 0
    for review in reviews:
        subtotal_rating+=review.rating
        if review.rating == 5:
            count5 +=1
        if review.rating == 4:
            count4 +=1
        if review.rating == 3:
            count3 +=1
        if review.rating == 2:
            count2 +=1
        if review.rating == 1:
            count1 +=1

    seller_ids = []
    for seller in vendors:
        seller_ids.append(seller.id)
    print(seller_ids)
    if len(reviews)>0:
        average_rating = subtotal_rating/len(reviews)
        length = len(reviews)
        # average_rating = get_rating_stars(average_rating)
    # average_rating = len(reviews)
   
    if length == 0:
        count5p = 0 
        count4p = 0
        count4p = 0
        count3p = 0 
        count2p = 0 
        count1p = 0
    else:
        count5p = count5/length 
        count4p = count4/length
        count3p = count3/length 
        count2p = count2/length 
        count1p = count1/length

    graphJSON = plot(product_id)
    return render_template('product_details.html', product = product, sellers = vendors, reviews = reviews, length = length, average_rating = average_rating, seller_ids = seller_ids,  count5= count5,  count4= count4,  count3= count3,  count2=  count2,  count1= count5, count5p = count5p, count4p = count4p, count3p = count3p, count2p = count2p,count1p = count1p, graphJSON=graphJSON)



def plot(product_id):
    order_ids = OrderP.get_order_sold_by_seller(product_id)
    
    sales_history =[]
    for order in order_ids:
        sales_hist=[order.firstname +" "+order.lastname[:1], order.total_quantity]
        print(sales_hist)
        sales_history.append(sales_hist)

    df = pd.DataFrame(sales_history,
                      columns=['Sellers', 'Sales'])
     
    # Create Bar chart
    fig = px.bar(df, x='Sellers', y='Sales', barmode='group')
     
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
    return graphJSON


def get_rating_stars(average_rating):
    full_star = '+'
    half_star = '-'
    round_half_rating = round(average_rating*2)/2

    if divmod(round_half_rating, 1)[1] == 0.5:
        return int(round_half_rating)*full_star + half_star
    else:
        return int(round_half_rating)*full_star


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Add')

@bp.route('/products/<product_id>/review', methods=['GET', 'POST'])
def addReview(product_id):
    product = Product.get(product_id)
    if not current_user.is_authenticated:
        flash("You need to log in!")
        return redirect(url_for('Product_Details.Product_Details', product_id = product_id))
    user_id = current_user.id

    ordered_product = OrderP.check_ordered_product(product_id, user_id)
    if not ordered_product:
        flash('You did not order this product.')
        return redirect(url_for('Product_Details.Product_Details', product_id = product_id))

    submitted_review = Review.check_submitted_review(product_id, user_id)
    if submitted_review:
        flash('You cannot submit multiple review for the same product.')
        return redirect(url_for('Product_Details.Product_Details', product_id = product_id))
    
    form = ReviewForm()
    time_post = datetime.now()
    if form.validate_on_submit():
        if Review.add_review(product_id, 
                            form.rating.data,
                            form.title.data,
                            form.content.data,
                            time_post):
            print(product_id)
        flash("Review Added Successfully")

    #if User.update_info(form.firstname.data, 
    #                    form.lastname.data, 
    #                    form.email.data,
    #                    form.mailingaddress.data):
    #    print(form.firstname.data)
    #    return redirect(url_for('users.updateInfo', uid=current_user.id))
    return render_template('add_review.html', product = product, form=form)