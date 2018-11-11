from os import abort

from flask import Flask, request, json, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


def do_the_login():
    return 'login successful'


def show_the_login_form():
    return 'trust me, this is login form'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' or request.method == 'GET':
        return do_the_login()
    else:
        return show_the_login_form()


@app.route('/checkout', methods=['POST'])
def checkout():
    if not request.json:
        abort(400)
    data = request.get_json(force=True)
    return jsonify(request.get_json(force=True))


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)