from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime
from app.extensions import DB
from app.extensions import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, DB.Model):

    id = DB.Column(DB.Integer, primary_key=True)
    
    username = DB.Column(DB.String(20), nullable = False, index=True, unique=True )

    email = DB.Column(DB.String(120), nullable = False, unique=True )

    image_file = DB.Column(DB.String(20), nullable=False, default='default.webp')

    password = DB.Column(DB.String(128), nullable = False)

    cash = DB.Column(DB.Float, default = 10000, nullable = False)

    port = DB.relationship('Portfolio', backref ='user', lazy = True)

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return '<User {} {}>'.format(self.username, self.email)


class Portfolio(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)

    stock = DB.Column(DB.String(30), nullable=False)

    quantity = DB.Column(DB.Integer, nullable=False)

    price = DB.Column(DB.Float(8,2), nullable = False)

    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return '<Portfolio ({}, {}, {})>'.format(self.stock, self.quantity, self.price)


class Stock_Transaction(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)

    stock = DB.Column(DB.String(30), nullable=False)

    quantity = DB.Column(DB.Integer, nullable=False)

    price = DB.Column(DB.Float(8,2), nullable = False)

    transaction_time = DB.Column(DB.DateTime, nullable=False, default = datetime.utcnow)

    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return '<Stock_Transaction ({}, {}, {}, {})>'.format(self.stock, self.quantity, self.price, self.transaction_time)