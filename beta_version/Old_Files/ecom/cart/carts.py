from flask import render_template,session, request,redirect,url_for,flash,current_app
from ecom import db , app
from ecom.products.models import Addproduct
from ecom.admin import routes

#Funtion to add the Addproduct db items with quantity and color attribute
def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

# Route to add elements to the cart
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image1, 'colors':product.color}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            # Set session that if same product if added to cart twice then only quantity updates 
                            # it will not update num in the cart(num) for same item added twice 
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
        pass
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

# Route for cart item display
@app.route('/carts')
def getCart():
    # if no items in cart it will guide user to product page
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('allproduct'))
    subtotal = 0
    grandtotal = 0
    # it will get the info. about all the items in the cart by iterating 
    for key,product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax =("%.2f" %(.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('product/carts.html',tax=tax, grandtotal=grandtotal)

# Route to update cart
# When any item in cart to be updated (only color and quantity can be updated )
# The page returns id for that cart item for updatation
@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!','success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

# Route to delete cart items
# Page will return id of cart element to be deleted
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

# Route to clear cart
@app.route('/clearcart')
def clearcart():
    try:
        # Pops out the session and makes the cart empty
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

# Route to checkout
@app.route('/checkout')
def checkout():
    if 'email' not in session:
        flash('Please Login First','danger')
        return redirect(url_for('login'))
    return render_template('product/checkout.html')