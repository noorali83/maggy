from decimal import Decimal

from application import db, application
from application.models import Card, User, UserSchema, School, CardSchema
from flask import request, jsonify


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
        if card.balance >= amount_in_decimal:
            card.balance = card.balance - amount_in_decimal
            db.session.commit()
            status = 'Approved'
        else:
            status = 'Declined'
            error = 'Insufficient balance, Please topup your card'
    else:
        error = 'Card not found'
        status = 'Card not found'

    return jsonify(status = status, error = error)


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


if __name__ == '__main__':
    application.run(host='charopy-local', port=5001, debug=True)
