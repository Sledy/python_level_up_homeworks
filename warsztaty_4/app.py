from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    abort
)
from itertools import chain
from datetime import datetime
import sqlite3, json

app = Flask(__name__)


DATABASE = 'database.db'

@app.route('/')
def main_view():
    return render_template('main.html')

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description})


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/cities', methods=['GET'])
def get_cities():
    db = get_db()
    data = db.execute('SELECT city FROM city ORDER BY city ASC').fetchall()
    print(type(data))
    data = list(chain(*data))
    return json.dumps(data)
    # return render_template('cities.html', cities=data)


@app.route('/cities/<string:country_name>', methods=['GET'])
def get_country_cities(country_name):
    db = get_db()
    if len(country_name) > 0:
        print(country_name)
        country_id = db.execute('''SELECT country_id FROM country WHERE
         country LIKE ?''', (country_name,)).fetchone()
        data = db.execute(
            'SELECT city FROM CITY WHERE country_id = ?', (country_id[0],))
    else:
        data = db.execute('SELECT city FROM city ORDER BY city ASC').fetchall()
    data = list(chain(*data))
    return json.dumps(data)


    #return render_template('cities.html', cities=data)


@app.route('/cities', methods=['POST'])
def post_city():
    data_to_post = request.get_json()
    db = get_db()
    # Finding index to INSERT command
    index = db.execute('SELECT * FROM city').fetchall()
    index = len(index) + 1
    # Getting time to insert
    time = datetime.now()
    list_of_countries_id = db.execute('''SELECT country_id
     FROM country''').fetchall()
    # List of countries' id to verify json
    list_of_countries_id = tuple(set(chain(*list_of_countries_id)))

    if data_to_post['country_id'] not in list_of_countries_id:
        error = {"error": "Invalid country_id"}
        return jsonify(error), 400

    db.execute('''INSERT INTO city (city_id, city, country_id, last_update)
     VALUES (?, ?, ?, ?)''', (index, data_to_post['city_name'],
                              data_to_post['country_id'], time,))
    db.commit()

    result = db.execute('''SELECT city_id, city, country_id FROM city
        WHERE city=?''', (data_to_post['city_name'], )).fetchall()

    result = tuple(chain(*result))
    to_json = {"country_id": result[2],
               "city_name": result[1],
               "city_id": result[0]
               }
    return jsonify(to_json), 201

@app.route('/lang_roles', methods=['GET'])
def count_languages():
    db = get_db()
    what_keys = db.execute('''SELECT  language_id FROM language
     ORDER BY language_id ASC''').fetchall()
    what_keys = tuple(chain(*what_keys))
    languages = db.execute('''SELECT name FROM language
        ORDER BY language_id ASC ''')
    languages = tuple(chain(*languages))
    sum_dict = {}
    for id, key in zip(what_keys, languages):

        temp_set = db.execute('''SELECT (COUNT(actor_id)*language_id)
         AS lang_count FROM film JOIN film_actor ON
          film.film_id=film_actor.film_id
          WHERE language_id=? GROUP BY title''', (id,)).fetchall()

        temp_set = list(chain(*temp_set))

        sum_dict[key] = int(sum(temp_set) / id)
        print(sum_dict)

    return jsonify(sum_dict)


if __name__ == '__main__':
    app.run(debug=True)
