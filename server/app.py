#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.route('/restaurants')
def get_restaurants():
    restaurants = Restaurant.query.all()
    get_restaurants = [restaurant.to_dict() for restaurant in restaurants]

    response = make_response(get_restaurants, 200)
    
    return response


@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurants_by_id(id):
    restaurants = Restaurant.query.filter(Restaurant.id == id).first()
    
    if not restaurants:
            return make_response({"error": "Restaurant not found"}, 404)
    
    else:
        if request.method == 'GET':       
            response = make_response(restaurants.to_dict(), 200)
            return response
        
        elif request.method == 'DELETE':        
            db.session.delete(restaurants)
            db.session.commit()
        
            response = make_response({"message": "Restaurant {id} deleted"}, 200)
            return response


@app.route('/pizzas')
def get_pizzas():
    pizzas = Pizza.query.all()
    get_pizzas = [pizza.to_dict() for pizza in pizzas]

    response = make_response(get_pizzas, 200)
    
    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
