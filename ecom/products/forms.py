from flask_wtf.file import FileAllowed,FileField,FileRequired
from wtforms import Form, StringField, PasswordField, validators,IntegerField,TextAreaField,DecimalField

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