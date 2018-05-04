from functools import wraps
from uuid import uuid4
from flask import (Flask, request, Response,
                   session, redirect, url_for, jsonify,
                   render_template)

from my_error import InvalidUsage

app = Flask(__name__)
app.secret_key = bytes.fromhex('aad123f1c23b27fb938200adbc23')

app.fishes = {}


def get_fish_from_json():
    fish_data = request.get_json()
    if not fish_data:
        raise InvalidUsage('Please provide json data')
    return fish_data


def set_fish(fish_id=None, data=None, update=False):
    if fish_id is None:
        fish_id = str(uuid4())

    if data is None:
        data = get_fish_from_json()
        if data is None:
            raise InvalidUsage('Please provide json data')

    if update:
        app.fishes[fish_id].update(data)
    else:
        app.fishes[fish_id] = data

    return fish_id


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def start():
    return 'Siemanko'


def check_auth(username, password):
    check = (username == 'Akwarysta69' and password == 'Jesiotr')
    return check


def please_authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_basic_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return please_authenticate()
        return func(*args, **kwargs)

    return wrapper


@app.route('/login', methods=['GET', 'POST'])
@requires_basic_auth
def login():
    session['username'] = request.authorization.username
    return redirect(url_for('hello'))


@app.route('/hello')
def hello():
    return render_template('greeting.html', user=session['username'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('start'))


@app.route('/fishes', methods=['GET', 'POST'])
def fishes():
    if request.method == 'GET':
        return jsonify(app.fishes)

    elif request.method == 'POST':
        fish_id = set_fish()
        return redirect(url_for('fish', fish_id=fish_id, format='json'))


@app.route('/fishes/<fish_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def fish(fish_id):
    if fish_id not in app.fishes:
        return 'Fish_id {} not found'.format(), 404

    if request.method == 'DELETE':
        del app.fishes[fish_id]
        return 'Fish with {} id number has been deleted'.format(fish_id), 204

    if request.method == 'PUT':
        set_fish(fish_id)

    if request.method == 'PATCH':
        set_fish(fish_id, update=True)

    if request.method == 'GET' and request.args.get('format') != 'json':
        raise InvalidUsage("Missing 'format=json' in query string",
                           status_code=415)

    return jsonify(app.fishes[fish_id])


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False)
