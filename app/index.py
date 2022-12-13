import math
from flask import redirect, render_template, request, url_for
from flask_login import current_user
import datetime
from flask import current_app as app
from app.Pagination import Pagination
from app.models.order import Order

from .models.product import Product
from flask_wtf import FlaskForm
from flask import Blueprint
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
bp = Blueprint('index', __name__)

class ProductSearch(FlaskForm):
    id = StringField('K', validators=[DataRequired()])
    submit = SubmitField('Search')

class ProductFilter(FlaskForm):
    id = StringField('K', validators=[DataRequired()])
    submit = SubmitField('Search')
    




ROWS_PER_PAGE = 10
@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ProductSearch()
    print("info")
    sort = request.form.getlist("sort")


    page = int(request.args.get('page', 1))
    search_key= request.args.get('search',"")
    sort_key= request.args.get('sort',"id_asc")
    category_key= request.args.get('filter',"all")
    show_available = request.args.get("available","false")

    filter = request.form.getlist("filter")

    available_only = request.form.getlist("available")
    print(available_only)
    if request.method == "POST":
        if len(sort) >0 :
            return redirect(url_for('index.index',search = search_key, sort = sort[0], filter = category_key, available = show_available))
        elif len(form.id.data)>0:
            return redirect(url_for('index.index',search = form.id.data, sort = sort_key, filter = category_key, available = show_available))
        elif len(filter)>0:
            return redirect(url_for('index.index',search = search_key, sort = sort_key, filter = filter[0], available = show_available))
        elif len(available_only)>0:
            return redirect(url_for('index.index',search = search_key, sort = sort_key, filter = category_key, available = "true"))

    
    
    if show_available == "true":
        show_available = True
    else:
        show_available = False


    category_names = Product.get_category_names()



    print(search_key)



    products = Product.get_products(search_key, category_key, sort_key, show_available, page=page,limit=ROWS_PER_PAGE)
    total_products = Product.get_total_products(search_key, page = page, limit = ROWS_PER_PAGE)

    totalPages = math.ceil(total_products/ROWS_PER_PAGE)



            
        
    if current_user.is_authenticated:
        purchases = None
        purchases = Order.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        print("is_authenticated")
        print(purchases)
    else:
        purchases = None
    # render the page by adding information to the index.html file

    print(sort_key)
    print(category_key)
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           pagination_total = totalPages,
                           page = page,
                           pagination_data = Pagination.get_pagination_values(page, totalPages),
                           selectedSort = sort_key,
                           category_names = category_names,
                           selected_category = category_key,
                           form = form)



