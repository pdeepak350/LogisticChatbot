from flask import redirect, url_for, render_template, request, flash, session, current_app
from ecom import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
from ecom.admin import routes
import os

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
	if session['email']!="admin@admin.com":
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
	if session['email']!="admin@admin.com":
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
	if session['email']!="admin@admin.com":
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
	if session['email']!="admin@admin.com":
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
	if session['email']!="admin@admin.com":
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
	if session['email']!="admin@admin.com":
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
	if session['email']!="admin@admin.com":
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
		addpro= Addproduct(name=name, price=price, discount=discount, stock=stock, color=color, desc=desc, brand_id=brand, category_id=category, image1=image1, image2=image2, image3=image3)
		db.session.add(addpro)
		flash(f'Product Added Successfully', 'success')
		db.session.commit()
		return redirect(url_for('addproduct'))
	return render_template('product/addproduct.html', form=form, brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
	if session['email']!="admin@admin.com":
		return redirect(url_for('home'))
	brands= Brand.query.all()
	categories= Category.query.all()
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
		db.session.commit()
		return redirect(url_for('admin'))
	form.name.data= product.name
	form.price.data= product.price
	form.discount.data= product.discount
	form.stock.data= product.stock
	form.color.data= product.color
	form.description.data= product.desc
	return render_template('product/updateproduct.html', form=form, brands=brands, categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=['GET', 'POST'])
def deleteproduct(id):
	if session['email']!="admin@admin.com":
		return redirect(url_for('home'))
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
