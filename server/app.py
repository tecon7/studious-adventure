#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Hero, HeroPower, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes')
def heroes():
    heroes = Hero.query.all()
    data = [hero.to_dict() for hero in heroes]
    return make_response(jsonify(data), 200)

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()
    if not hero:
        return make_response(jsonify({
            'error': 'Hero not found'
        }))
    return make_response(jsonify(hero.to_dict()), 200)


@app.route('/powers')
def powers():
    powers = Power.query.all()
    data = [power.to_dict() for power in powers]
    return make_response(jsonify(data), 200)

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):
    power = Power.query.filter(Power.id == id).first()
    if not power:
        return make_response(jsonify({
            'error': 'Power not found'
        }))
    if request.method == 'GET':
        return make_response(jsonify(power.to_dict()), 200)
    elif request.method == 'PATCH':
        data = request.get_json()
        for field, value in data.items():
            setattr(power, field, value)
        db.session.add(power)
        db.session.commit()
        return make_response(jsonify(power.to_dict()), 200)

@app.route('/hero_powers', methods=['POST'])
def hero_powers():
    data = request.get_json()
    new_hp = HeroPower(
        strength=data['strength'],
        power_id=data['power_id'],
        hero_id=data['hero_id']
    )
    db.session.add(new_hp)
    db.session.commit()
    return make_response(jsonify(new_hp.to_dict()), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
