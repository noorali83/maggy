from datetime import datetime

from application import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_num = db.Column(db.String(20), index=True, unique=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)

    def __init__(self, card_num, status, created_date):
        self.card_num = card_num
        self.status = status
        self.created_date = created_date


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), index=True, unique=False)
    expiry_date = db.Column(db.String(20), unique=False)
    balance = db.Column(db.Numeric(10,2))
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)

    def __init__(self, number, expiry_date, balance, status='ACITVE') -> None:
        super().__init__()
        self.number = number
        self.expiry_date = expiry_date
        self.balance = balance
        self.status = status

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
