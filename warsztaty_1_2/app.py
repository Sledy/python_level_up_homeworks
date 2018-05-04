from flask import Flask, request, render_template, make_response
from flask import redirect, url_for, g, session, jsonify, abort
from datetime import datetime
from functools import wraps
from user_agents import parse

app = Flask(__name__)
app.secret_key = 'safsadf@#!131241@#QWEDSDFE$'
app.counter = 0


@app.route('/')
def main():
    return 'Hello, World!'


#
#
# Drugie warsztaty
#
#
#


# słownik zs loginem i hasłem
user = {'Akwarysta69': 'J3si07r'}

fishes = {
    "id_1": {
        "who": "Znajomy",
        "where": {
            "lat": 0.001,
            "long": 0.002
        },
        "mass": 34.56,
        "length": 23.67,
        "kind": "szczupak"
    },
    "id_2": {
        "who": "Kolega kolegi",
        "where": {
            "lat": 34.001,
            "long": 52.002
        },
        "mass": 300.12,
        "length": 234.56,
        "kind": "sum olimpijczyk"
    }
}


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if (auth and auth.username == 'Akwarysta69' and
                auth.password == user['Akwarysta69'] and
                session['islogin'] == True):

            return f(*args, **kwargs)

        return redirect(url_for('login'))

    return decorated


@app.route('/now')
@auth_required
def date():
    now = datetime.now()
    return "{}".format(now)


@app.route('/user-agent')
@auth_required
def user_agent():
    ua = parse(request.headers.get('User-Agent'))
    print(str(request.headers))
    return str(ua)

@app.route('/counter')
@auth_required
def counter():
    app.counter += 1
    return '{}'.format(app.counter)

# Function that pops out to log in


@app.route('/login')
def login():
    flag = session.get('islogin', False)
    if (request.authorization and
        request.authorization.username == 'Akwarysta69' and
            request.authorization.password == user['Akwarysta69']):
        session['islogin'] = True
        return redirect(url_for("hello"))

    return make_response('Could not verify your login !', 401,
                         {'WWW-Authenticate': 'Basic realm=""Login Required'})


@app.route('/logout')
@auth_required
def logout():
    # g.islogin = False
    session['islogin'] = False
    return 'logut'


@app.route('/page')
@auth_required
def page():
    return '<h1> You are on the page </h1>'


@app.route('/hello')
@auth_required
def hello():
    return render_template('greeting.html',
                           user=request.authorization.username)


@app.route('/fishes', methods=['GET'])
@auth_required
def get_fishes():
    return jsonify({'fishes': fishes})


@app.route('/fishes/<id>', methods=['POST'])
@auth_required
def post_fishes(id):
    # if not request.json or not 'title' in request.json:
     #   abort(400)
    fish = {
        "who": request.json["who"],
        "where": {
            "lat": request.json['where']["lat"],
            "long": request.json['where']["long"]
        },
        "mass": request.json["mass"],
        "length": request.json["length"],
        "kind": request.json["kind"]
    }
    fishes[id] = fish

    return jsonify({'fishes': fishes}), 201


@app.route('/fishes/<id>', methods=['GET'])
@auth_required
def particular_fish(id):
    return jsonify({'fishes': fishes[id]})


@app.route('/fishes/<id>', methods=['PUT'])
@auth_required
def update_fishes(id):
    if not request.json:
        abort(400)
    fishes[id]['who'] = request.json.get('who')
    fishes[id]['where']['lat'] = request.json.get('lat')
    fishes[id]['where']['long'] = request.json.get('long')
    fishes[id]['mass'] = request.json.get('mass')
    fishes[id]['length'] = request.json.get('length')
    fishes[id]['kind'] = request.json.get('kind')

    return jsonify({'fishes': fishes[id]})


@app.route('/fishes/<id>', methods=['DELETE'])
@auth_required
def delete_fish(id):
    del fishes[id]
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
