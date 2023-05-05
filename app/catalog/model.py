from app import db,bcrpt
from datetime import datetime
from app import login_manager
from flask_login import UserMixin


class Publication(db.Model):
    
     id = db.Column(db.Integer, primary_key = True) 
     name = db.Column(db.String(100),nullable = False)
    
     def __init__(self,name):
         self.name = name
    
     def __repr__(self): #return string representation of the item
       return "Publisher Name : {} ".format(self.name)

     def insertPublication(punName):
       # id=idNum,name=punName to avoid init error
        pub = Publication(name=punName) # instance of table
        #// use instance of DB ti add
        db.session.add(pub)
        db.session.commit()
        
     def updatePublisherName(id):
         pub = Publication.query(id)
         pub.name = input("Please enter new Publisher name \n")   
         db.session.commit()   
          
        
class Book(db.Model):
     
     id = db.Column(db.Integer, primary_key = True) 
     title = db.Column(db.String(500), nullable =False, index=True)   
     author = db.Column(db.String(350))
     avg_rating = db.Column(db.Float)
     format = db.Column(db.String(50))
     image_path = db.Column(db.String(110),unique=True)
     num_pages = db.Column(db.Integer)
     pub_date = db.Column(db.DateTime, default= datetime.utcnow()) 
     #relationship
     pub_id = db.Column(db.Integer, db.ForeignKey("publication.id"))
     
     def __init__(self,title,author,avg_rating,format,image_path,num_pages,pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = format
        self.image_path = image_path
        self.num_pages = num_pages
        self.pub_id = pub_id
        
     def __repr__(self): #return string representation of the item
           return "TITLE : {}, By : {} ".format(self.title,self.author)    
        
     def insertBooks(btitle,bauthor,bavg_ratings,bformat,bimage_path,bnum_pages,bpub_id):
       # id=idNum,name=punName to avoid init error
        bk = Book(title=btitle,author =bauthor,avg_rating=bavg_ratings,format = bformat,
                  image_path=bimage_path,num_pages=bnum_pages,pub_id=bpub_id)
        #// use instance of DB ti add
        db.session.add(bk)
        db.session.commit() 
        
     def getAllBooks():
        books = Book.query.all() 
        return books

     def getFirstBook():# first record in th table
      book = Book.query.first() 
      return book

     def getAllBooksType():
            return Book.query.filter_by(format="Paperback" ).all()  
     def getAllBooksByTitle():
            return Book.query.filter_by(format="Paperback" ).order_by(Book.title).all()
     
     def updateBookName(id):
         id = int(input("Please Enter book ID \n"))
         bookId = Book.query.get(id)
         bookId.title = input("Please enter new Book name \n")   
         db.session.commit()  
            
     def deleteBook(id): #silgle row delete
         return Book.query.get(id)
         
         
     def deleteAllByIdBook(id=0): # multi row delete: if there is a foreign ker constraint, the record would hve to be deleter first in the other table
         id = int(input("Please Enter book ID \n"))
         Book.query.filter_by(pub_id =id).delete() 
         db.session.commit()
         
class User(UserMixin,db.Model):
     
     id = db.Column(db.Integer, primary_key = True)  
     user_name = db.Column(db.String(20))
     user_email = db.Column(db.String(60),unique = True, index =True)
     password = db.Column(db.String(128))
     registration_date = db.Column(db.DateTime, default= datetime.utcnow()) 
     
     #not belong to an instance cls instead of self os of class
     @classmethod
     def createUser(cls,user,email,password):
          user = cls(user_name = user,
                    user_email = email,
                    password = bcrpt.generate_password_hash(password).decode("utf-8")
                    )  
          print("USER ",user)                 
          db.session.add(user)
          db.session.commit()
          return user
     
     def check_password(self,password):
          return bcrpt.check_password_hash(self.password,password)
          
        
     @classmethod  
     def getUser(cls,user_name):
        # check if user name exists
         userName = User.query.filter_by(user_name = user_name).first()
         if (userName == user_name):
             return True
      
     @classmethod  
     def getUserEmail(cls,user_email):
         # check if user with email exists
         return User.query.filter_by(user_email = user_email).first()
    
           
     @login_manager.user_loader  
     def uder_loader(id):
       return User.query.get(int(id))    