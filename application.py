from decimal import Decimal

from Emailparser import EmailParser
from Topup import Topup
from application import db, application
from application.models import Card, User, UserSchema, School, CardSchema, Transaction, TransactionSchema, SchoolSchema, \
    SchoolSchemaLite
from flask import request, jsonify
import simplejson as json


@application.route('/api/checkout', methods=['POST'])
def checkout():
    req_data = request.get_json()

    cardNumber = req_data['cardNumber']
    amount = req_data['amount']
    amount_in_decimal = Decimal(amount.replace(',', '.'))
    card = Card.query.filter_by(number=cardNumber).first()

    error = None
    status = None

    if card is not None:
        student_id = card.owner_id
        card_owner = User.query.filter_by(id=student_id).first()
        if card_owner is None:
            status = 'Declined'
            error = 'Card not associated to any user'
        else:
            if card_owner.balance >= amount_in_decimal:
                card_owner.balance = card_owner.balance - amount_in_decimal
                redeem_txn = Transaction(card_num=card.number, type='REDEEM', amount=amount_in_decimal,
                                         status='APPROVED')
                db.session.add(redeem_txn)
                db.session.commit()
                status = 'Approved'
            else:
                status = 'Declined'
                error = 'Insufficient balance, Please topup your card'
    else:
        error = 'Card not found'
        status = 'Declined'

    return jsonify(status=status, error=error)


@application.route('/api/users', methods=['GET'])
def users():
    users = User.query.order_by(User.id.desc()).limit(100).all()
    users = UserSchema(many=True).dump(users).data
    return jsonify(users)


@application.route('/api/cards', methods=['GET'])
def cards():
    cards = Card.query.limit(100).all()
    cards = CardSchema(many=True).dump(cards).data
    return jsonify(cards)


@application.route('/api/transactions', methods=['GET'])
def transactions():
    transactions = Transaction.query.limit(100).all()
    transactions = TransactionSchema(many=True).dump(transactions).data
    return jsonify(transactions)


@application.route('/api/schools', methods=['GET'])
def schools():
    schools = School.query.limit(100).all()
    schools = SchoolSchema(many=True).dump(schools).data
    return jsonify(schools)


@application.route('/api/schools/<school_name>', methods=['GET'])
def school(school_name):
    school = School.query.filter_by(name=school_name).first()
    return SchoolSchemaLite().jsonify(school)

@application.route('/api/topup/refresh', methods=['GET'])
def refresh_topups():

    topups = EmailParser().get_topups()

    topup_1 = Topup("5555444433332000", "100.00", "12/20", "Noor", "KHSS" )
    topup_2 = Topup("5555444433332001", "100.00", "12/20", "Muhammad Ali", "Darcy Road School" )
    topup_3 = Topup("5555444433332002", "100.00", "12/20", "Muhammad Ali", "KHSS" )

    #topups = [topup_1, topup_2, topup_3]

    for topup in topups:
        school = None
        user = None
        card = None
        school = School.query.filter_by(name=topup.school_name).first()
        if school is not None:
            user = User.query.filter_by(name=topup.customer_name, school=school).first()
            if user is not None:
                card = Card.query.filter_by(number=topup.card_num).first()
                if card is None:
                    card = Card(number=topup.card_num, expiry_date=topup.card_expiry_date, owner_id=user.id)
                    db.session.add(card)
                    db.session.commit()

                user.balance = user.balance + Decimal(topup.amount.replace(',', '.'))
                db.session.add(user)
                db.session.commit()
            else:
                user = User(name=topup.customer_name, school=school, balance=topup.amount)
                db.session.add(user)
                db.session.commit()
                card = Card(number=topup.card_num, expiry_date=topup.card_expiry_date, owner_id=user.id)
                db.session.add(card)
                db.session.commit()
        else:
            school = School(name=topup.school_name)
            db.session.add(school)
            db.session.commit()
            user = User(name=topup.customer_name, school=school, balance=topup.amount)
            db.session.add(user)
            db.session.commit()
            card = Card(number=topup.card_num, expiry_date=topup.card_expiry_date, owner_id=user.id)
            db.session.add(card)
            db.session.commit()

    return jsonify(status="Success", error=None)

if __name__ == '__main__':
    application.run(host='charopy-local', port=5001, debug=True)
