from .forms import RegistrationForm, LoginForm
from flask import render_template, request, redirect, url_for, flash, session
from .models import User
from ecom import app, db, bcrypt, login_manager
from flask_login import login_user,login_required,current_user,logout_user
from ecom.products.models import Addproduct,Brand,Category

# Route for user and admin to home page
@app.route("/")
@app.route("/home")
def home():
    # fetches the new 5 products from database Addproduct 
    # You can change limit to any number you want
    products=Addproduct.query.order_by(Addproduct.id.desc()).limit(5).all()
    return render_template('home.html',products=products)

# Route for admin only to manage the products
@app.route("/admin",methods=['GET','POST'])
def admin():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if session['email']!="admin@admin.com":
        return redirect(url_for('home'))
    #fetches all the products from the database
    products=Addproduct.query.all()
    return render_template('admin/manage.html',products=products)

#Route for admin only to manage the brands
@app.route("/brands",methods=['GET','POST'])
def brands():
    if 'email' not in session:
        flash(f'Please Login First','success')
        return redirect(url_for('login'))
    if session['email']!="admin@admin.com":
        return redirect(url_for('home'))
    #fetches all brands from the database Brand in descending order
    brands=Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html',brands=brands)

#Route for admin only to manage the categories
@app.route("/categories",methods=['GET','POST'])
def categories():
    if 'email' not in session:
        flash(f'Please Login First','success')
        return redirect(url_for('login'))
    if session['email']!="admin@admin.com":
        return redirect(url_for('home'))
    # fetches all the categories from Category table in descending order
    categories=Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/category.html',categories=categories)

# Route for login page
@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        next = request.args.get('next')
        return redirect(next or url_for('home'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('This user not exists','warning')
            return redirect(url_for('login'))
        #Validates and authenticates user
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #Set session on top of cookies with 'email' parameter set to email of user entered
            session['email'] = form.email.data
            flash('Logged in successfully.','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Invalid password','danger')
    return render_template('login.html', form=form)

# Route to logout user
@app.route('/logout')
# It works only when any user is in the system
@login_required
def logout():
    # Pops out the email parameter set for the logged in user
    session.pop('email',None)
    logout_user()
    flash('You are Logged Out','danger')
    return redirect(url_for('login'))

#Route for signup 
@app.route('/signup', methods=['GET', 'POST'])
def SignUp():
    # Get data from the Registration Form
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data,
                    email=form.email.data, password=hash_password)
        db.session.add(user)
        # Adds user permanently in the database
        db.session.commit()
        flash(
            f'Welcome {form.username.data} Thanks for registering', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)