## app init file
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_bootstrap import Bootstrap5
#from flask import Markup
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# instance of the database
db = SQLAlchemy()
bcrpt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "main.login" #login method
login_manager.session_protection = "strong" #protect user session
#bootstrap = Bootstrap5()

def create_app(config_type): #dev test prod
    app = Flask(__name__)
    #path of configuration path
    configuration = os.path.join(os.getcwd(),"config",config_type+".py")
    app.config.from_pyfile(configuration)
     #attach to db instance
    db.init_app(app)
    login_manager.init_app(app)
    bcrpt.init_app(app)
    #bootstrap.init_app(app)
   
    #register blueprint
    from app.catalog import main
    app.register_blueprint(main)
   # from app.auth import authentication
   # app.register_blueprint(authentication)

    return app