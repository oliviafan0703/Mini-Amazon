from flask import jsonify, render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
import json
from sqlalchemy import JSON
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, DataRequired

from flask import Blueprint

from app.models.product import Product
from app.models.user import User
from app.models.order import Order

bp = Blueprint('carts', __name__)

class CartsForm(FlaskForm):
    id = StringField('UserID', validators=[DataRequired()])
    submit = SubmitField('Save ID')

class EditCartForm(FlaskForm):
    new_quantity = IntegerField('new_quantity', validators=[DataRequired('Please enter a new quantity!')])
    submit = SubmitField('Save')

class CouponCartForm(FlaskForm):
    coupon = StringField('Coupon Code', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # def validate_coupon(self, coupon):
    #     if coupon == "minitaobao":
    #         raise ValidationError('Not a valid Coupon')

@bp.route('/cart_add', methods=['GET', 'POST'])
def cart_add():
    if not current_user.is_authenticated:
        return {"error":"Not Logged In"}, 201
    print("current user:")
    print(current_user.id)
    if request.method == "POST":
        print(request.data)
        cartData = json.loads(request.data)

    print("object")
    product_id = cartData["product_id"]
    print(product_id)
    for seller_id, qty in cartData["data"].items():
        print(seller_id,qty)
        Product.add_cart_item(qty,product_id,seller_id,current_user.id)

    #success code
    #flash("Successfully add to cart!")
    return {"success":"successful"}, 201
        
@bp.route('/carts', methods=['GET', 'POST'])
def carts():
    # form = CartsForm()
    # targetID = form.id.data
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))
    products = Product.get_user_cart(current_user.id)
    total_before_discount = sum([item.price * item.quantity for item in products])
    total_before_discount = round(total_before_discount, 2)
    total = sum([item.price * item.quantity for item in products])


    #apply discounts here:
    num_products = len(products)
    for item in products:
       if item.quantity >=20:
           total = round(total*0.8,2)
        #    flash("Congrats, you got 20 percent discounts")
       if item.quantity >=10:
           total = round(total*0.9,2)
        #    flash("Congrats, you got 10 percent discounts")
    print(products)
            
    x_ids = []
    seller_id = []
    for item in products:
        x_ids.append(str(item.seller_id)+"_"+str(item.product_id))
        print (item.seller_id)
        print (item.product_id)
        seller_id.append(item.seller_id)
        # sellers.append(Cart.get_sellers_by_product(item.seller_id))
        # print(Cart.get_sellers_by_product(item.seller_id))
        
    
    return render_template('cart.html', cart_data=products, total = total, x_ids = x_ids, seller_id = seller_id, total_before_discount= total_before_discount)

@bp.route('/submit_order', methods=['GET', 'POST'])
def submit_order():

    #     products = Product.get_user_cart(current_user.id)
    # if len(products) > 0:
    #     flash("Congratulations, you successfully ")
    # else:
    #     flash("Sorry, No Item in Cart!!")    
    # return redirect(url_for('carts.carts'))

    if request.method == "POST":
        cartData = json.loads(request.data)

    print(cartData)
    #print(cartData['39_10'])
    cart = cartData['cart'].items()
    print("submit order called!")
    print(cart)
    total = cartData['total_price']
    # if quantity >= 10:
    #     total = total * 0.9

    # for product_id, product in cart.items():
        
    #     seller_id = product.seller_id
    #     quantity = product.quantity
    #     """
    #     do this at the loading of checkout page 
    #     """

    #made updates
    current_cart = Product.get_user_cart(current_user.id)

    canPurchase = True
    for product in current_cart:
        inventory = Product.get_seller_inventory(product.seller_id, product.product_id)
        if inventory<product.quantity:
            # print("there is enough")
            # print(total)
            # print(current_user.balance)
            canPurchase = False
            flash("Not Enough Inventory!")
            info={"error": "Seller does not have enough inventory!"}
            return info, 200
        #check if enough money
        if current_user.balance < total:
            canPurchase = False 
            print(total)
            print(current_user.balance)
            flash("Insufficient Funds!")
            info={"error": "Insufficient Funds!"}
            print("bad")
            return info, 200

    if not canPurchase:
        flash("Unable to purchase product")
        return "Unable to purchase product", 200
        
    User.pay(total)
    order_id = Order.create_order()
    print("orderid")
    print(order_id)

    for product in current_cart:
        remainingInventory = Product.remove_from_inventory(product.seller_id, product.product_id, product.quantity)
        print(f'remaininginventory: {remainingInventory}')
        Product.remove_cart_item(product.product_id, product.seller_id, current_user.id)
        Order.add_to_order(order_id, product.product_id, product.seller_id, product.quantity)
        subtotal = product.price*product.quantity
        User.credit(subtotal, product.seller_id)



    #create order 
    

    #proceed to purchase 
    print("Enough Funds. and Can Purchase")
    
    
    # if len(current_cart) > 0:
    #     flash("Congratulations, you successfully purchased")

    info = {"error": "Successfully Purchase"}
    #flash("Successfully Purchase")
    print("got here")

    return info, 200

@bp.route('/save_cart', methods=['GET', 'POST'])
def save_cart():
    #get the updated quantities in cart, and reflect those. 
    
    if request.method == "POST":
        cartData = json.loads(request.data)
    
    # print(cartData['39_10'])
    items = cartData['cart'].items()
    print(len(items))

    #move this up! :
    if len(items) < 1:
        flash("Sorry, No Item In Cart!")
        info = {"error": "Sorry, No Item In Cart!"}
        return info, 200

    # if items[1] >= 10:
    #     flash("Congrats! You got 10 percent discounts on total price!")
    for item in items:
        x_id = item[0]
        quantity = item[1]
        splits = x_id.split("_") 
        seller_id = splits[0]
        product_id = splits[1]
        #flash("Cart Saved!")
        print(Product.update_cart_item_qty(seller_id, product_id, current_user.id, quantity))
    return {"message": "Cart Saved Successfully"}, 201

@bp.route('/edit_item', methods=['GET', 'POST'])
def edit_item():
    form = EditCartForm()

    products = Product.get_user_cart(current_user.id)
    if form.validate_on_submit():
        flash('You have successfully edited this item!')
    else:
        flash("Sorry, no enough inventory")
    return redirect(url_for('carts.carts'))
    #return render_template('cart.html', form=form)

@bp.route('/remove_item', methods=['GET', 'POST'])
def remove_item():
    print("got here")
    products = Product.get_user_cart(current_user.id)
    
    pid = request.args['pid']
    sid = request.args['sid']
    print("product_id")
    print(pid)
    print("seller_id")
    print(sid)


    Product.remove_cart_item(pid, sid, current_user.id)
    return redirect(url_for('carts.carts'))



# @bp.route('/checkout_api', methods=['GET', 'POST'])
# def checkout_api():
#     print(request.method)
#     if request.method == "POST":
#         cartData = json.loads(request.data)
#     print(cartData)
#     uid = current_user.id 
#     profile_user = User.get(uid)
#     cartData= {}


#     return "",201

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    uid = current_user.id 
    profile_user = User.get(uid)
    products = Product.get_user_cart(current_user.id)
    total_before_discount = sum([item.price * item.quantity for item in products])
    total_before_discount = round(total_before_discount, 2)
    total = sum([item.price * item.quantity for item in products])


    #apply discounts here:
    num_products = len(products)
    for item in products:
       if item.quantity >=20:
           total = round(total*0.8,2)
        #    flash("Congrats, you got 20 percent discounts")
       if item.quantity >=10:
           total = round(total*0.9,2)
        #    flash("Congrats, you got 10 percent discounts")
    print(products)


    processed_products = {}
    for product in products :
        processed_products[product.product_id] = {
            'name':product.product_name,
            'quantity': product.quantity,
            'price': product.price,
            'seller_id': product.seller_id,
            'product_id': product.product_id
        }
    
    print(processed_products)

    return render_template('checkout.html', profile_user = profile_user, products = processed_products, total = total, num_products = num_products, total_before_discount = total_before_discount)

@bp.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')


@bp.route('/cart', methods=['GET', 'POST'])
def coupon():
    products = Product.get_user_cart(current_user.id)
    total_before_discount = sum([item.price * item.quantity for item in products])
    total_before_discount = round(total_before_discount, 2)
    total = sum([item.price * item.quantity for item in products])

     #apply discounts here:
    num_products = len(products)
    for item in products:
       if item.quantity >=20:
           total = round(total*0.8,2)
        #    flash("Congrats, you got 20 percent discounts")
       if item.quantity >=10:
           total = round(total*0.9,2)
        #    flash("Congrats, you got 10 percent discounts")
    print(products)

    uid = current_user.id 
    profile_user = User.get(uid)

    processed_products = {}
    for product in products :
        processed_products[product.product_id] = {
            'name':product.product_name,
            'quantity': product.quantity,
            'price': product.price,
            'seller_id': product.seller_id,
            'product_id': product.product_id
        }
    
    print(processed_products)

    form = CouponCartForm()
    if form.validate_on_submit():
        if form.coupon.data == "minitaobao":
            total_new = round(total * 0.8,2)
            flash('Congrats You have got New Year Coupon')
            print(total)
            return render_template('checkout.html', profile_user = profile_user, products = processed_products, total = total, num_products = num_products, total_before_discount = total_before_discount, total_new = total_new)
        else:
            flash("Sorry this Coupon does not work!!")
    print("total")
    print(total)
    return render_template('coupon.html', title='Coupon', form=form, total = total)