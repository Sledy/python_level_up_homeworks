from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    abort,
    current_app
)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from generated_code import Base, City, Country
import json
from datetime import datetime
from functools import wraps


app = Flask(__name__)

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def main_view():
    return render_template('main.html')


@app.route('/cities', methods=['GET'])
def get_cities():
    all_cities = session.query(City).all()
    list_of_cities = [city.city for city in all_cities]
    sorted(list_of_cities)
    return json.dumps(list_of_cities)


@app.route('/cities/<string:country_name>', methods=['GET'])
def one_city(country_name):
    id_search = (session.query(Country)
                 .filter(Country.country == country_name).one())

    id_search = id_search.country_id
    cities = (session.query(City).filter(City.country_id == id_search)
              .all())

    list_of_cities = [city.city for city in cities]
    sorted(list_of_cities)
    return json.dumps(list_of_cities)


@app.route('/cities', methods=['POST'])
def post_cities():

    data_to_post = request.get_json()
    country_id = [country_name[0]
                  for country_name in session.query(Country.country_id)]
    if ((data_to_post['country_id'] not in country_id)):
        raise InvalidUsage('Invalid country_id', status_code=400)
    new_city = City(city=data_to_post['city_name'],
                    country_id=data_to_post['country_id'])
    session.add(new_city)
    # Showing result
    result = session.query(City).filter(
        City.city == data_to_post['city_name'],
        City.country_id == data_to_post['country_id']).first()
    print(result.city, result.country_id, result.city_id)
    dict_result = {'city_name': result.city,
                   "city_id": result.city_id,
                   "country_id": result.country_id
                   }
    session.commit()
    return json.dumps(dict_result)


if __name__ == '__main__':
    app.run(debug=True)
