from flask import Response, render_template, redirect, session, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_security import login_required

from .models.user import User
from .models.review import Review
from app.models.product import Product


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    mailingaddress = StringField("Mailing Address",validators=[DataRequired()])
    checkbox = BooleanField('Also register as seller?')
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.mailingaddress.data,
                         form.checkbox.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Change Password')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

@bp.route("/change_password", methods=["GET", "POST"])
def change_password():
    form = ChangePasswordForm()
    print("got")
    if form.validate_on_submit():
        print("in")
        if User.update_password(form.password.data):
            print("here")
            print(form.password.data)
    return render_template("change_password.html", form=form)

@bp.route('/logout')
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        # prevent flashing automatically logged out message
        del session['was_once_logged_in']
    session.clear()
    # response = Response(
    #                 is_redirect=True,
    #                 url=url_for('index.index'))
    # 
    # return response
    response = redirect(url_for('index.index'))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

class ProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mailingaddress = StringField("Mailing Address",validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/profile/me', methods=['GET', 'POST'])
def profile():
    profile_user = User.get(current_user.id)
    is_seller = User.is_seller(current_user.id)
    seller_addr = User.get_address(current_user.id) 
    reviews = Review.get_seller_reviews(current_user.id)
    return render_template("profile.html", is_seller=is_seller, profile_user=profile_user,
                            seller_addr=seller_addr, reviews=reviews)


class BalanceForm(FlaskForm):
    balance = FloatField('First Name', default=0.0, validators=[NumberRange(0, 1E+20)])

@bp.route('/update/me', methods=['GET', 'POST'])
def updateInfo():
    form = ProfileForm()
    profile_user = User.get(current_user.id)
    if request.method == "POST":
        if(User.email_exists(form.email.data)):
            if(form.email.data != profile_user.email):
                flash("email already in use")
        if User.update_info(form.firstname.data, 
                                form.lastname.data, 
                                form.email.data,
                                form.mailingaddress.data):
            print(form.firstname.data)
            flash("Information Changed Successfully!")
            return redirect(url_for("users.updateInfo"))
    return render_template('edit_profile.html',form = form, profile_user = profile_user)

@bp.route('/add/me', methods=['GET', 'POST'])
def addBalance():
    profile_user = User.get(current_user.id)
    form = BalanceForm()
    User.add_money(form.balance.data)
    if(request.method == "POST"):
        flash("Successfully Added Funds!")
    return render_template('balance.html',profile_user=profile_user)

@bp.route('/withdraw/me', methods=['GET', 'POST'])
def withdrawBalance():
    profile_user = User.get(current_user.id)
    form = BalanceForm()
    exceed_balance = User.check_exceed_balance(form.balance.data)
    if exceed_balance:
        flash('Invalid. Amount to withdraw exceeded balance.')
    else:
        User.withdraw_money(form.balance.data)
        if(request.method == "POST"):
            flash("Successfully Withdrew Funds!") 


    return render_template('withdraw.html',profile_user=profile_user)

class ProductForm(FlaskForm):
    Category = StringField('Category', validators=[DataRequired(message = "Please enter a valid category number!")])
    Name = StringField('Name', validators=[DataRequired(message = "Please enter a valid name!")])
    Price = StringField('Price', validators=[DataRequired(message = "Please enter a valid price number!")])
    Description = StringField('Description', validators=[DataRequired(message = "Please enter a valid description!")])
    Image_url = StringField('Image_url', validators=[DataRequired(message = "Please enter a valid image url!")])
    Quantity = StringField('Quantity', validators=[DataRequired(message = "Please enter a valid quantity!")])
    submit = SubmitField('Save')

@bp.route('/create_product', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        if Product.create_product(form.Name.data, form.Image_url.data, form.Price.data, form.Description.data, form.Category.data, form.Quantity.data):
            flash('Congratulations, you successfully created the product!')
            return redirect(url_for('index.index'))
    return render_template('create_product.html', form = form)

@bp.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    form = ProductForm()
    if form.validate_on_submit():
        if Product.edit_product(product_id, form.Name.data, form.Image_url.data, form.Price.data, form.Description.data, form.Category.data, form.Quantity.data):
            flash('Congratulations, you successfully edited the product!')
            return redirect(url_for('index.index'))
    return render_template('edit_product.html', form = form, seller_id = current_user.id)
