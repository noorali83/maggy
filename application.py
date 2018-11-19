from os import abort
from application import db, application
from application.models import Transaction, Card, School, User, UserSchema
from flask import request, jsonify


@application.route('/checkout', methods=['POST'])
def checkout():
    if not request.json:
        abort(400)
    data = request.get_json(force=True)
    return jsonify(request.get_json(force=True))


@application.route('/api/users', methods=['GET'])
def users():
    users = User.query.order_by(User.id.desc()).limit(100).all()
    users = UserSchema(many=True).dump(users).data
    return jsonify(users)

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=5001, debug=True)