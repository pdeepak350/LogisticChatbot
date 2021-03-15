from wtforms import Form, StringField, PasswordField, validators

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
