# from flask import current_app
# from flask_sqlalchemy import SQLAlchemy

# app=current_app
# db=SQLAlchemy(app)
# db.init_app(app)

# class User(db.Model):
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name=db.Column(db.String, nullable=False, unique=True) #This name is username
#     # full_name=db.Column(db.String, nullable=False)
#     password=db.Column(db.String, nullable=False)
#     role=db.Column(db.String)


# class Category(db.Model):
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name=db.Column(db.String, nullable=False, unique=True)

# class Product(db.Model):
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name=db.Column(db.String, nullable=False, unique=True)
#     exp_date=db.Column(db.DateTime(), nullable=False)
#     rate_per_unit=db.Column(db.Integer, nullable=False)
#     qnt_avl=db.Column(db.Integer)
#     categories=db.relationship('category', backref='product')

# class Order_item(db.Model):
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ordered_quantity=db.Column(db.Integer, nullable=False)
#     order_total=db.Column(db.Integer)
#     orders=db.relationship('Order', backref='order_item')

# class Order(db.Model):
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     order_total=db.Column(db.Integer)
#     order_items_id=db.Column(db.Integer, db.ForeignKey('order_item.id'), nullable=False)
#     user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
