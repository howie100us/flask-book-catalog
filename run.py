from app import create_app,db
from app.catalog.model import User
## execute applications



if __name__ == "__main__":
    flask_app = create_app("prod")
    #create db tables
    with flask_app.app_context():
         db.create_all()
                   
         flask_app.run()