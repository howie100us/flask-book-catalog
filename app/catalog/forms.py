#from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email
import email_validator

class RegistrationForm():
    
    name = ""
    email = ""
    submit = ""

class LoginForm():
    email = StringField("Email", validators = [DataRequired(),Email()])
    password = PasswordField("Password",validators = [DataRequired()])
    stay_loggedin = BooleanField("stay logged-in")
    submit = SubmitField("LogIn")
    
class EditBookForm():
    title = StringField("Title", validators = [DataRequired()])
    format = StringField("Format", validators = [DataRequired()])
    num_pages = StringField("Pages", validators = [DataRequired()])
    submit = SubmitField("Update")
