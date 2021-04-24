from wtforms import Form, StringField, PasswordField, validators, IntegerField, TextAreaField, DecimalField
from flask_wtf.file import FileAllowed,FileField,FileRequired

# Registration form for signup page with following fields
class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=2, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField(
        'Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(
    ), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')

# Login Form for login page with following fields
#Validators are used to validate data submitted by user and checks validations
class LoginForm(Form):
    email = StringField(
        'Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])

# Form to add product 
# All the fields are required to fill and 3 imags of product needs to be uploaded
class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount=IntegerField('Discount',default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    color=TextAreaField('Colors',[validators.DataRequired()])
    description=TextAreaField('Description',[validators.DataRequired()])
    image1=FileField('Image_1',validators=[FileAllowed(['jpg','png','jpeg','gif']),'only images supported'])
    image2=FileField('Image_2',validators=[FileAllowed(['jpg','png','jpeg','gif']),'only images supported'])
    image3=FileField('Image_3',validators=[FileAllowed(['jpg','png','jpeg','gif']),'only images supported'])
    merchant_id = IntegerField('Merchant ID', [validators.DataRequired()])
    merchant_name = StringField('Merchant Name', [validators.DataRequired()])
    merchant_phone = DecimalField('Merchant Phone', [validators.DataRequired()])
    merchant_address = TextAreaField('Merchant Address',[validators.DataRequired()])