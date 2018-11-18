from datetime import datetime

from application import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_num = db.Column(db.String(20), db.ForeignKey('card.number'), index=True, unique=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), default=0.00)


class Card(db.Model):
    number = db.Column(db.String(20), index=True, primary_key=True)
    expiry_date = db.Column(db.String(20), unique=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transactions = db.relationship('Transaction')

    def add_balance(self, top_up_amount):
        self.balance = self.balance + top_up_amount

    def getAmount(self):
        return self.balance

    def getCardNumber(self):
        return self.number

    def has_sufficient_balance(self, purchase_amount):
        return self.balance - purchase_amount >= 0

    def deduct_balance(self, purchase_amount):
        self.balance = self.balance - purchase_amount


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)
    students = db.relationship('User', backref='school')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    cards = db.relationship('Card', backref='owner')
