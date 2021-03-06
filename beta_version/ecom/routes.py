from flask import render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user,login_required,current_user,logout_user
from .models import Admin, Cart, Merchant, User, Brand, Category, Addproduct, Delivery, Shipment
from .forms import RegistrationForm, LoginForm, Addproducts
from ecom import app, db, bcrypt, login_manager, photos
from sqlalchemy.sql import text
import os
from datetime import datetime, timedelta
import random
import string

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
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
        return redirect(url_for('home'))
    #fetches all the products from the database
    products=Addproduct.query.all()
    return render_template('admin/manage.html',products=products)

@app.route("/merchant", methods=['GET', 'POST'])
def merchant():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    merchant = Merchant.query.filter_by(email=session['email']).first()
    if merchant is None:
        return redirect(url_for('home'))
    #fetches all the products from the database
    merchant_id = merchant.id
    #merchant_id = str(merchant_id)
    products=Addproduct.query.filter_by(merchant_id=merchant_id).all()
    print(products)
    return render_template('admin/manage.html',products=products)

#Route for admin only to manage the brands
@app.route("/brands",methods=['GET','POST'])
def brands():
    if 'email' not in session:
        flash(f'Please Login First','success')
        return redirect(url_for('login'))
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
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
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
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

@app.route('/contact')
def contact():
    return render_template('contact.html' )

# Route for user and admin to see all products in the system
@app.route('/allproduct',methods=['GET','POST'])
def allproduct():
	# It displays first page on starting
	page=request.args.get('page',1,type=int)
	# On each page it will display 4 products
	# You can change it by changing per_page attribute
	products= Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page,per_page=4)
	categories=Category.query.join(Addproduct,(Category.id==Addproduct.brand_id)).all()
	return render_template('product/index.html',products=products,categories=categories)

# Route for admin and user which displays single product description
# On clicking View Description an id of product is sent to this page to proceed
@app.route('/single/<int:id>',methods=['GET','POST'])
def single(id):
	product=Addproduct.query.get_or_404(id)
	return render_template('product/singleProd.html',product=product)

# Route for user and admin to see products filtered by their categories
# An id is passed when user choose category to display
@app.route('/filtercat/<int:id>', methods=['GET', 'POST'])
def filtercat(id):
	get_cat_prod=Addproduct.query.filter_by(category_id=id)
	categories=Category.query.join(Addproduct,(Category.id==Addproduct.brand_id)).all()
	return render_template('product/index.html',categories=categories,get_cat_prod=get_cat_prod)

# Route for admin only
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
        return redirect(url_for('home'))
    if request.method == "POST":
		# Adds new brand to system which is added by admin
        getbrand= request.form.get('brand')
        brand= Brand(name=getbrand)
        db.session.add(brand)
        flash(f'{getbrand} Successfully added', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('product/addbrand.html', brand="brand")

# Route for admin only
@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
        return redirect(url_for('home'))
    updatebrand= Brand.query.get_or_404(id)
	# it will fetch brand name from form and replace it with old one
    brand= request.form.get('brand')
    if request.method == "POST":
        updatebrand.name= brand
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('product/updatebrandandcategory.html', updatebrand=updatebrand)

# Route for admin only
# to delete a brand an id of brand is returned to this route
@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
        return redirect(url_for('home'))
    brand= Brand.query.get_or_404(id)
    if request.method == "POST":
		# it will delete the brand from the system
        db.session.delete(brand)
        db.session.commit()
        return redirect(url_for('brands'))
    return redirect(url_for('brands'))


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
        return redirect(url_for('home'))
    if request.method == "POST":
        getcat= request.form.get('category')
        cat= Category(name=getcat)
        db.session.add(cat)
        flash(f'{getcat} Successfully added', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('product/addbrand.html')

@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
        return redirect(url_for('home'))
    updatecat= Category.query.get_or_404(id)
    category= request.form.get('category')
    if request.method == "POST":
        updatecat.name= category
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('product/updatebrandandcategory.html', updatecat=updatecat)

@app.route('/deletecategory/<int:id>', methods=['GET', 'POST'])
def deletecategory(id):
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
        return redirect(url_for('home'))
    cat= Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(cat)
        db.session.commit()
        return redirect(url_for('categories'))
    return redirect(url_for('categories'))

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    admin = Admin.query.filter_by(email=session['email']).first()
    merchant = Merchant.query.filter_by(email=session['email']).first()
    if admin is None and merchant is None:
        return redirect(url_for('home'))
    brands= Brand.query.all()
    categories= Category.query.all()
    form= Addproducts(request.form)
    if request.method == "POST":
        name= form.name.data
        price= form.price.data
        discount= form.discount.data
        stock= form.stock.data
        color= form.color.data
        desc= form.description.data
        brand= request.form.get('brand')
        category= request.form.get('category')
        image1= photos.save(request.files.get('image1'))
        image2= photos.save(request.files.get('image2'))
        image3= photos.save(request.files.get('image3'))
        merchant_id = form.merchant_id.data
        merchant_name = form.merchant_name.data
        merchant_phone = form.merchant_phone.data
        merchant_address = form.merchant_address.data
        addpro= Addproduct(name=name, price=price, discount=discount, stock=stock, color=color, desc=desc, brand_id=brand, category_id=category, image1=image1, image2=image2, image3=image3, merchant_id=merchant_id, merchant_name=merchant_name, merchant_phone=merchant_phone, merchant_address=merchant_address)
        db.session.add(addpro)
        flash(f'Product Added Successfully', 'success')
        db.session.commit()
        return redirect(url_for('addproduct'))
    return render_template('product/addproduct.html', form=form, brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    admin = Admin.query.filter_by(email=session['email']).first()
    merchant = Merchant.query.filter_by(email=session['email']).first()
    if admin is None and merchant is None:
        return redirect(url_for('home'))
    brands= Brand.query.all()
    categories= Category.query.all()
    if admin is None:
        product= Addproduct.query.filter_by(id=id,merchant_id=merchant.id).all()
        for i in product:
            product=i
    elif merchant is None:
        product= Addproduct.query.get_or_404(id)
    brand= request.form.get('brand')
    category= request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name= form.name.data
        product.price= form.price.data
        product.discount= form.discount.data
        product.brand_id= brand
        product.category_id= category
        product.color= form.color.data
        product.desc= form.description.data
        if request.files.get('image1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/img/"+product.image1))
                product.image1= photos.save(request.files.get('image1'))
            except:
                product.image1= photos.save(request.files.get('image1'))
        if request.files.get('image2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/img/"+product.image2))
                product.image2= photos.save(request.files.get('image2'))
            except:
                product.image2= photos.save(request.files.get('image2'))
        if request.files.get('image3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/img/"+product.image3))
                product.image3= photos.save(request.files.get('image3'))
            except:
                product.image3= photos.save(request.files.get('image3'))
        if admin is None:
            product.merchant_id = merchant.id
        elif merchant is None:
            product.merchant_id = form.merchant_id.data
        product.merchant_name = form.merchant_name.data
        product.merchant_phone = form.merchant_phone.data
        product.merchant_address = form.merchant_address.data
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data= product.name
    form.price.data= product.price
    form.discount.data= product.discount
    form.stock.data= product.stock
    form.color.data= product.color
    form.description.data= product.desc
    form.merchant_id.data = product.merchant_id
    form.merchant_name.data = product.merchant_name
    form.merchant_phone.data = product.merchant_phone
    form.merchant_address.data = product.merchant_address
    return render_template('product/updateproduct.html', form=form, brands=brands, categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=['GET', 'POST'])
def deleteproduct(id):
    admin = Admin.query.filter_by(email=session['email']).first()
    merchant = Merchant.query.filter_by(email=session['email']).first()
    if admin is None and merchant is None:
        return redirect(url_for('home'))
    if admin is None:
        product= Addproduct.query.filter_by(id=id,merchant_id=merchant.id).all()
        for i in product:
            product=i
    elif merchant is None:
        product= Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/img/"+product.image1))
            os.unlink(os.path.join(current_app.root_path, "static/img/"+product.image2))
            os.unlink(os.path.join(current_app.root_path, "static/img/"+product.image3))
        except Exception as e:
            print("Something Bad happened : ", e)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))

#Funtion to add the Addproduct db items with quantity and color attribute
def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

# Route to add elements to the cart
@app.route('/addcart', methods=['POST'])
def AddCart():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        try:
            user_id = session['_user_id']
            product_id = request.form.get('product_id')
            quantity = int(request.form.get('quantity'))
            color = request.form.get('colors')

            if request.method =="POST":
            #if 'Shoppingcart' in session:
                cart = Cart.query.filter_by(user_id=user_id, product_id=product_id, color=color).first()
                if cart is None:
                    addcart = Cart(user_id=user_id, product_id=product_id, color=color, quantity=quantity)
                    db.session.add(addcart)
                    db.session.commit()
                    
                else:
                    #if product_id in session['Shoppingcart']:
                    cart = Cart.query.filter_by(user_id=user_id, product_id=product_id, color=color).first()
                    cart_id = cart.id
                    cart_color = cart.color
                    ct = Cart.query.filter_by(id=cart_id, user_id=user_id, product_id=product_id, color=cart_color).first()
                    ct.quantity = ct.quantity + quantity
                    db.session.commit()
            pass
                  
        except Exception as e:
            print(e)
        finally:
            return redirect(request.referrer)
            
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

# Route for cart item display
@app.route('/carts')
def getCart():
    #DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image1, 'colors':product.color}}
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        #if 'Shoppingcart' not in session:
        #    return redirect(url_for('allproduct'))
        cart_items={}
        user_id = session['_user_id']
        cart = Cart.query.order_by(text(user_id)).all()
        for i in cart:
            temp_cart={}
            product=Addproduct.query.filter_by(id=i.product_id).first()
            id = str(i.product_id) + '_' + str(i.id)
            temp_cart = {id:{'id':i.id, 'name':product.name,'price':float(product.price),'discount':product.discount,'color':i.color,'quantity':i.quantity,'image':product.image1, 'colors':product.color}}
            cart_items = Merge(cart_items, temp_cart)

        #if no items in cart it will guide user to product page
        subtotal = 0
        grandtotal = 0
        # it will get the info. about all the items in the cart by iterating
        try:
            for key,product in cart_items.items():
                product_id = int(key.split('_')[0])
                discount = (product['discount']/100) * float(product['price'])
                subtotal += float(product['price']) * int(product['quantity'])
                subtotal -= discount
                tax =("%.2f" %(.06 * float(subtotal)))
                grandtotal = float("%.2f" % (1.06 * subtotal))
                # print(session['Shoppingcart'].items())  
            return render_template('product/carts.html',tax=tax, grandtotal=grandtotal, cart_items=cart_items, product_id=product_id)
        except Exception as e:
            print(e)
            flash(f'no items in cart', 'error')
            return redirect(url_for('allproduct'))


@app.route('/orderplaced', methods=['GET','POST'])
def orderplaced():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        try:
            user_id = session['_user_id']
            # cart_items = request.form.get('cart_items')
            cart_items = Cart.query.filter_by(user_id=user_id).all()
            print(type(cart_items[0]))
            print(cart_items[0])
            for i in cart_items:
                print(i.user_id)
            if request.method =="POST":
            #if 'Shoppingcart' in session:
                for i in cart_items:
                    product_id = i.product_id
                    merchant = Addproduct.query.filter_by(id=product_id).first()
                    user = User.query.filter_by(id=user_id).first()
                    delivery_reg_time = datetime.now()
                    delivery_est_date = datetime.now().date() + timedelta(7)
                    delivery_id = '#'+ran_gen()
                    delivery = Delivery(User_id=i.user_id ,product_id=product_id, merchant_id=merchant.merchant_id,color='black', quantity=i.quantity ,Delivery_ID=delivery_id,Delivery_Reg_Time=delivery_reg_time ,Delivery_Est_Date=delivery_est_date,Delivery_Sender=merchant.merchant_name,Delivery_Sender_Phone=merchant.merchant_phone, From_Address= merchant.merchant_address, Delivery_Recipient = user.name, Delivery_Recipient_Phone='000000', To_Address='Virginia - VA-20006 - USA', Status_Reason='Order Placed')
                    db.session.add(delivery)
                    db.session.commit()
                    ship_id = '#'+ran_gen(size=9)
                    shipment = Shipment(Shipment_ID=ship_id, Shipment_Note=random.choices(['processing','shipped','delivered'])[0], Delivery_ID=delivery_id)
                    db.session.add(shipment)
                    db.session.commit()
            pass
                  
        except Exception as e:
            print(e)
        finally:
            return redirect(url_for('clearcart'))
# Route to update cart

# When any item in cart to be updated (only color and quantity can be updated )
# The page returns id for that cart item for updatation
@app.route('/updatecart/<int:code>', methods=['GET', 'POST'])
def updatecart(code):
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        cart = Cart.query.filter_by(id=code).first()
        try:
            cart.quantity = quantity
            cart.color = color
            db.session.commit()
            flash('Item is updated!','success')
            return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            flash('updated cart', 'success')
            return redirect(url_for('getCart'))

# Route to delete cart items
# Page will return id of cart element to be deleted
@app.route('/deleteitem/<int:id>', methods=['GET', 'POST'])
def deleteitem(id):
    if request.method=="POST":
        cart = Cart.query.filter_by(id=id).first()
        try:
            db.session.delete(cart)
            db.session.commit()
            flash(f'deleted item', 'success')
            return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

# Route to clear cart
@app.route('/clearcart')
def clearcart():
    try:
        user_id = session['_user_id']
        cart = Cart.query.order_by(text(user_id)).all()
        for i in cart:
            db.session.delete(i)
            db.session.commit()
        flash(f'Order Placed', 'success')
        return redirect(url_for('allproduct'))
    except Exception as e:
        print(e)
        flash(f'Success', 'success')
        return redirect(url_for('allproduct'))

@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        delivery_items={}
        user =User.query.filter_by(email=session['email']).first()
        user_id=session['_user_id']
        delivery = Delivery.query.filter_by(User_id=user_id).all()
        subtotal = 0
        grandtotal = 0
        for i in delivery:
            temp_delivery = {}
            product=Addproduct.query.filter_by(id=i.product_id).first()
            id = str(i.product_id) + '_' + str(i.Delivery_ID)
            discount = (product.discount/100) * float(product.price)
            subtotal += float(product.price) * int(i.quantity)
            subtotal -= discount
            tax =("%.2f" %(.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal))
            temp_delivery = {id:{'id':i.Delivery_ID, 'name':product.name, 'price':float(product.price),'qunatity':i.quantity,'placed_on':i.Delivery_Reg_Time ,'est_date':i.Delivery_Est_Date , 'address':i.To_Address, 'image':product.image1} }
            delivery_items = Merge(delivery_items, temp_delivery)
    return render_template('profile.html', user=user, delivery=delivery_items, tax=tax, grandtotal=grandtotal, subtotal=subtotal)

def ran_gen( size=7 , chars=string.ascii_letters+string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def shipment(delivery_id):
    try:
        ship_id = '#'+ran_gen(size=9)
        shipment = Shipment(Shipment_ID=ship_id, Shipment_Note=random.choices(['processing','shipped','delivered'])[0], Delivery_ID=delivery_id)
        db.session.add(shipment)
        db.session.commit()
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/manage/<string:delivery_id>', methods=['GET', 'POST'])
def manage_order(delivery_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        delivery_items={}
        user =User.query.filter_by(email=session['email']).first()
        delivery = Delivery.query.filter_by(Delivery_ID=delivery_id).all()
        subtotal = 0
        grandtotal = 0
        for i in delivery:
            temp_delivery = {}
            product=Addproduct.query.filter_by(id=i.product_id).first()
            id = str(i.product_id) + '_' + str(i.Delivery_ID)
            discount = (product.discount/100) * float(product.price)
            subtotal += float(product.price) * int(i.quantity)
            subtotal -= discount
            tax =("%.2f" %(.06 * float(subtotal)))
            grandtotal = float("%.2f" % (1.06 * subtotal))
            temp_delivery = {id:{'id':i.Delivery_ID, 'name':product.name, 'price':float(product.price),'qunatity':i.quantity,'placed_on':i.Delivery_Reg_Time ,'est_date':i.Delivery_Est_Date , 'address':i.To_Address, 'image':product.image1} }
            delivery_items = Merge(delivery_items, temp_delivery)
            shipment(i.Delivery_ID)
    return render_template('profile.html', user=user, delivery_items=delivery_items, tax=tax, grandtotal=grandtotal, subtotal=subtotal)

@app.route('/merchantprofile')
def merchantprofile():
    if 'email' not in session:
        return redirect(url_for('login'))
    merchant = Merchant.query.filter_by(email=session['email']).first()
    if merchant is None:
        return redirect(url_for('home'))
    return render_template('merchantprofile.html')
    
@app.route('/adminprofile')
def adminprofile():
    if 'email' not in session:
        return redirect(url_for('login'))
    admin = Admin.query.filter_by(email=session['email']).first()
    if admin is None:
        return redirect(url_for('home'))
    return render_template('adminprofile.html')

# Route to checkout
@app.route('/checkout')
def checkout():
    if 'email' not in session:
        flash('Please Login First','danger')
        return redirect(url_for('login'))
    return render_template('product/checkout.html')
    
