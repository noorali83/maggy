from decimal import Decimal

from application import db, application
from application.models import Card, User, UserSchema, School, CardSchema, Transaction, TransactionSchema
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


if __name__ == '__main__':
    application.run(host='charopy-local', port=5001, debug=True)
