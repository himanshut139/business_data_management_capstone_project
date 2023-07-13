from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///groceasy_database.sqlite3"
app.config['SECRET_KEY'] = 'groceasysecretkey'

engine = None
Base = declarative_base()

db = SQLAlchemy(app)
db.init_app(app)

class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False, unique=True)
    password=db.Column(db.String, nullable=False)
    role=db.Column(db.String)

class Category(db.Model):
    __tablename__="category"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False, unique=True)
    # product_id=db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    # products=db.relationship('Product', backref='category')
    
class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False, unique=True)
    exp_date=db.Column(db.DateTime(), nullable=False)
    rate_per_unit=db.Column(db.Integer, nullable=False)
    qnt_avl=db.Column(db.Integer)
#     categories=db.relationship('category', backref='product')

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html") 

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        username=request.form['username']
        pwd=request.form['password']

        try:
            user=User.query.filter(User.name==username, User.password==pwd, User.role=="user").one()
        except:
            return render_template('login.html', error='Incorrect Username or Password')
        session["user"]=username
        return redirect("/user/dashboard")
    
@app.route("/admin/login", methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template("admin_login.html")
    if request.method == 'POST':
        username=request.form['user_name']
        pwd=request.form['password']
        try:
            user=User.query.filter(User.name==username, User.password==pwd, User.role=='admin').one()
        except:
            return render_template('admin_login.html')
        session["user"]=username
        return redirect("/admin/dashboard")
    
@app.route('/user/dashboard', methods=['GET','POST'])
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/logout')
def logout():
    print(session)
    if "user" in session:
        session.pop("user", None)
        flash("You have been logged out!")
    return redirect(url_for("home"))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        user_name=request.form['username']
        pwd=request.form['password']

        if user_name not in [x.name for x in User.query.all()]:
            user=User(name=user_name, password=pwd, role="user")
            db.session.add(user)
            db.session.commit()
            session['user']=user_name
            # flash("Successfully Signed Up")
            return render_template('login.html')
        return redirect('/notfound/User already exists.')
    return render_template('signup.html')

@app.route('/create/category', methods=['GET', 'POST'])
def create_category():
    if request.method=='POST':
        c_name=request.form['c_name']

        cat=Category(name=c_name)

        db.session.add(cat)
        db.session.commit()
        return redirect('/categories')
    return render_template('create_category.html')

@app.route("/categories")
def view_categories():
    all_categories=Category.query.all()
    return render_template("view_categories.html", all=all_categories) 

@app.route('/add/product', methods=['GET','POST'])
def add_product():
    # if "user" in session and session["user"].role=='admin':
    if request.method=='POST':
        p_name=request.form['prod_name']
        ex_date=request.form['expiry_date']
        rate_p_unit=request.form['unit_rate']
        avl_qnt=request.form['qnt_avl']
        ex_date=datetime.strptime(ex_date,"%Y-%m-%d")

        prdct=Product(name=p_name, exp_date=ex_date, rate_per_unit=rate_p_unit, qnt_avl=avl_qnt)

        db.session.add(prdct)
        db.session.commit()
        return redirect('/view/products')

    return render_template('add_product.html')

@app.route("/view/products")
def view_products():      #THIS ONE IS FOR ADMIN
    all_products=Product.query.all()
    return render_template("view_products.html", all=all_products) 

@app.route("/admin/dashboard")
def admin_dashboard():
    # all_categories=Category.query.all()
    return render_template("admin_dashboard.html") 

@app.route('/c_id=<category_id>/delete/category')
def delete_category(category_id):
    cat = Category.query.filter_by(id=category_id).first()
    db.session.delete(cat)
    db.session.commit()
    return redirect("/categories")

@app.route("/products")
def products():
    all_products=Product.query.all()
    return render_template("products.html", all=all_products) 

@app.route('/p_id=<product_id>/delete/product')
def delete_product(product_id):
    prdct = Product.query.filter_by(id=product_id).first()
    db.session.delete(prdct)
    db.session.commit()
    return redirect("/products")


# @app.route("/user=<username>/adding_category", methods=['GET','POST'])
# def adding_category(username):
#     if "user" in session and session["user"].role=='admin':
#         if request.method=='POST':
#             c_name=request.form['name']

#             if c_name not in [x.name for x in Category.query.all()]:
#                 cat=Category(name=c_name)
#                 db.session(cat)
#                 db.session.commit()
#                 return admin_dashboard()
#             return "Category already exists"
#         return render_template('adding_category.html')
        
@app.route('/c_id=<category_id>/update/category', methods=['GET','POST'])
def update_category(category_id):
    cat = Category.query.filter_by(id=category_id).first()
    # if "user" in session and session["user"].role=='admin':
    if request.method=="POST":
        new_name=request.form["newname"]
        print(new_name)

        if new_name=='':
            return "Category name cannot be blank."
        if new_name!=cat.name:
            cat.name=new_name
            db.session.commit()
            return redirect("/categories")
    return render_template('update_category.html', id=category_id)
    # return 'Only admin can access this.'

@app.route('/p_id=<product_id>/update/product', methods=['GET','POST'])
def update_product(product_id):
    prdct = Product.query.filter_by(id=product_id).first()
    # if "user" in session and session["user"].role=='admin':
    if request.method=="POST":
        new_name=request.form["newname"]
        new_exp=request.form["newexp"]
        new_rate=request.form["newrpu"]
        new_avl_qnt=request.form["newqntavl"]

        if new_name!=prdct.name:
            Product.name=new_name
            Product.exp_date=new_exp
            Product.rate_per_unit=new_rate
            Product.qnt_avl=new_avl_qnt
            db.session.commit()
            return redirect("/products")
    return render_template('update_product.html')
    # return 'Only admin can access this.'

# @app.route('/user=<username>/user_dashboard/')
# def user_dashboard(username):
#     user = User.query.filter_by(name=username).first()
#     if "user" in session and session["user"] == user.username:
#         return render_template("user_dashboard.html")
#     else:
#         return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)