from app.catalog import main
from app import db
from app.catalog.model import Book, Publication,User
from flask import render_template,request,flash,redirect,url_for
from app.catalog.forms import RegistrationForm,LoginForm,EditBookForm
from flask_login import login_user,logout_user,login_required,current_user


@main.route("/")
def displatBooks():
   books = Book.getAllBooks()
   return render_template("home.html",books = books)


@main.route("/display/publisher/<publish_id>")
def displayPubId(publish_id):
    publisher = Publication.query.filter_by(id=publish_id).first() # first pub id
    publisher_books = Book.query.filter_by(pub_id = publish_id).all() ## all books pudlish by this publisher
    return render_template("publisher.html",publisher = publisher,publisher_books =publisher_books)

@main.route("/login", methods = ["GET","POST"])
def login():
   if current_user.is_authenticated:
      return redirect(url_for("main.displatBooks"))
   
   form = LoginForm()
   if request.method == "POST":
      email = request.form["email"] 
      password = request.form["password"] #get password
      user = User.getUserEmail(email) #get user
   
      if not user or not user.check_password(password): #check email and password
       flash("Invalidate Crendentials Please try again")
       return redirect(url_for("main.login"))
   #from flas login
      elif login_user(user,form.stay_loggedin) == True:
       return redirect(url_for("main.displatBooks")) 
   else:
      return render_template("login.html")
   
@main.route("/logout")
@login_required
def logout():
    logout_user() ## inbuilt function that delets the session of the user
    return redirect(url_for("main.login"))
 
@main.route("/book/delete/<book_id>",methods = ["GET","POST"])
@login_required
def deleteBook(book_id):
    book = Book.query.get(book_id)
    print("METHODS ",request.method )
    if request.method == "POST":
      db.session.delete(book) # delete book and commit
      db.session.commit()
      return redirect(url_for("main.displatBooks")) 
    else:
      return render_template("delete.html",book = book,book_id = book.id)


@main.route("/register", methods = ["GET","POST"])
def home():
    if current_user.is_authenticated:
      return redirect(url_for("main.displatBooks"))
   # form = RegistrationForm()
    
    if request.method == "POST":
        user = request.form["name"]
        email_address = request.form["email"]
        
        name = User.getUser(request.form["name"])
        email = User.getUserEmail(request.form["email"])
        if name.user_email == user:
           flash(user," Already Exists!")
           return redirect(url_for("main.home"))
       
        elif name.user_email == user: 
           User.createUser(user = request.form["name"],email = request.form["email"],password = request.form["password"])
           print("Registration Successful !")
           return redirect(url_for("main.login"))
      
    return render_template("test.html")
 
@main.route("/book/edit/<book_id>",methods = ["GET","POST"])
@login_required
def editBook(book_id):
   
   book = Book.query.get(book_id)
   form = EditBookForm()
   if request.method =="POST":
   #get book info to edit
    book.title = request.form["title"]
    book.format = request.form["format"]
    book.num_pages = request.form["num_pages"]
    #add changes to db and commit
    db.session.add(book)
    db.session.commit()
    return redirect(url_for("main.displatBooks"))
   
   else:
      return  render_template("edit.html",book = book) 
   
   
@main.route("/book/add",methods = ["GET","POST"])
@login_required
def addBook():
  
   if request.method =="POST":
    book = Book(
      request.form["title"],
      request.form["author"],
      request.form["avg_rating"],
      request.form["format"],
      request.form["image_path"],
      request.form["num_pages"],
      request.form["pub_id"])
    #add changes to db and commit
    db.session.add(book)
    db.session.commit()
    return redirect(url_for("main.displatBooks"))
   
   else:
      return  render_template("book.html")  
   
@main.app_errorhandler(404)
def pageNotfounf(error):
    return render_template("404.html")