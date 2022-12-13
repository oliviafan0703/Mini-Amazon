from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models.user import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from app.models.product import Product
from datetime import datetime
from flask import Blueprint

from app.models.review import Review
bp = Blueprint('Reviews', __name__)


class ReviewsForm(FlaskForm):
    id = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route('/Reviews', methods=['GET', 'POST'])
def getProductReviews():
    profile_user = User.get(current_user.id)
    reviews = Review.get_user_reviews(current_user.id)
    return render_template('review.html', returned_productreviews=reviews)

@bp.route('/remove_review', methods=['GET', 'POST'])
def remove_review():
    pid = request.args['pid']
    print("product_id")
    print(pid)
    Review.delete_review(pid, current_user.id)

    return redirect(url_for('Reviews.getProductReviews'))

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')

@bp.route('/edit_review', methods=['GET', 'POST'])
def edit_review():
    product_id = request.args['product_id']
    rating = request.args['rating']
    content = request.args['content']
    title = request.args['title']
    product_name= request.args['product_name']

    form = ReviewForm()
    time_post = datetime.now()
    print("editing reviews")
    if request.method == "POST":
            
        if Review.editReview(current_user.id,
                                product_id,
                                form.rating.data,
                                form.title.data, form.content.data, time_post):
            print("success")      
        profile_user = User.get(current_user.id)
        reviews = Review.get_user_reviews(current_user.id)
        return render_template('review.html', returned_productreviews=reviews)
        
    #if User.update_info(form.firstname.data, 
    #                    form.lastname.data, 
    #                    form.email.data,
    #                    form.mailingaddress.data):
    #    print(form.firstname.data)
    #    return redirect(url_for('users.updateInfo', uid=current_user.id))
    return render_template('edit_review.html',form = form, rating=rating, content=content, title=title, product_name=product_name)

    
@bp.route('/upvote/<product_id>/<user_id>', methods=['GET', 'POST'])
def upvote(product_id,user_id):
    # product_id = request.args['product_id']
    reviews = Review.upvote(user_id, product_id)
    return redirect(url_for('Product_Details.Product_Details', product_id=product_id))
   
@bp.route('/downvote/<product_id>/<user_id>', methods=['GET', 'POST'])
def downvote(product_id,user_id):
    # product_id = request.args['product_id']
    reviews = Review.downvote(user_id, product_id)
    return redirect(url_for('Product_Details.Product_Details', product_id=product_id))
