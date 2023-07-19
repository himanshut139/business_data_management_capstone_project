from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from applications.database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///groceasy_database.sqlite3"
app.config['SECRET_KEY'] = 'groceasysecretkey'
app.config['UPLOAD_FOLDER'] = "./static/img/"

db.init_app(app)
app.app_context().push()


# from data import *



# class User(db.Model):
#     __tablename__="user"
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name=db.Column(db.String, nullable=False, unique=True)
#     password=db.Column(db.String, nullable=False)
#     role=db.Column(db.String)

# class Category(db.Model):
#     __tablename__="category"
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name=db.Column(db.String, nullable=False, unique=True)
#     # product_id=db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     # products=db.relationship('Product', backref='category')
    
# class Product(db.Model):
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name=db.Column(db.String, nullable=False, unique=True)
#     exp_date=db.Column(db.DateTime(), nullable=False)
#     rate_per_unit=db.Column(db.Integer, nullable=False)
#     qnt_avl=db.Column(db.Integer)
# #     categories=db.relationship('category', backref='product')

# with app.app_context():
#     db.create_all()





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
        


# @app.route('/user=<username>/user_dashboard/')
# def user_dashboard(username):
#     user = User.query.filter_by(name=username).first()
#     if "user" in session and session["user"] == user.username:
#         return render_template("user_dashboard.html")
#     else:
#         return redirect(url_for("login"))

from applications.controllers import *

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)