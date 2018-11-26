from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import fields

from application import application, db

ma = Marshmallow(application)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_num = db.Column(db.String(20), db.ForeignKey('card.number'), index=True, unique=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), default=0.00)


class TransactionSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'card_num', 'created_date', 'status', 'type', 'amount')


class Card(db.Model):
    number = db.Column(db.String(20), index=True, primary_key=True)
    expiry_date = db.Column(db.String(20), unique=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transactions = db.relationship('Transaction')


class CardSchema(ma.ModelSchema):
    class Meta:
        model = Card


class CardSchemaLite(ma.ModelSchema):
    class Meta:
        fields = ('number', 'status')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    cards = db.relationship('Card', backref='owner')


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class UserSchemaLite(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'balance', 'cards')
    cards = ma.Nested(CardSchemaLite, many=True, allow_null=True, default=tuple())


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=False)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False)
    students = db.relationship('User', backref='school')


class SchoolSchema(ma.ModelSchema):
    class Meta:
        model = School


class SchoolSchemaLite(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'students')

    students = ma.Nested(UserSchemaLite, many=True, allow_null=True, default=tuple())
