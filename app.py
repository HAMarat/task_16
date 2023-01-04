import sqlalchemy
from json.decoder import JSONDecodeError
from flask import jsonify, request
from utils import add_data_to_user, add_data_to_order, add_data_to_offer, serialize_user
from config import app, db
from models import User, Order, Offer

with app.app_context():
    db.drop_all()
    db.create_all()

add_data_to_user()
add_data_to_order()
add_data_to_offer()


@app.route('/users', methods=['GET', 'POST'])
def return_users():
    if request.method == 'GET':
        result = []
        users = db.session.query(User).all()
        for user in users:
            result.append(user.get_user())
        return jsonify(result)

    elif request.method == 'POST':
        try:
            db.session.add(serialize_user(request.json))
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as error:
            return f'{error}'
        return jsonify(code=200)


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def return_user_by_id(user_id):
    if request.method == 'GET':
        user = db.session.query(User).get(user_id)
        if user:
            return jsonify(user)
        return f"Пользователь с id {user_id} не найден"

    elif request.method == 'PUT':
        db.session.query(User).get(user_id).get_user()
        db.session.add(serialize_user(request.json))
        db.session.commit()
        return jsonify(code=200)

    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify(code=200)


@app.route('/orders', methods=['GET', 'POST'])
def return_orders():
    result = []
    orders = db.session.query(Order).all()
    for order in orders:
        result.append(order.get_order())
    return jsonify(result)


@app.route('/orders/<int:orders_id>', methods=['GET', 'PUT', 'DELETE'])
def return_order_by_id(orders_id):
    order = db.session.query(Order).get(orders_id).get_order()
    return jsonify(order)


@app.route('/offers', methods=['GET', 'POST'])
def return_offers():
    result = []
    offers = db.session.query(Offer).all()
    for offer in offers:
        result.append(offer.get_offer())
    return jsonify(result)


@app.route('/offers/<int:offers_id>', methods=['GET', 'PUT', 'DELETE'])
def return_offer_by_id(offers_id):
    offer = db.session.query(Offer).get(offers_id).get_offer()
    return jsonify(offer)


@app.errorhandler(404)
def error_404(error):
    return "Страница не найдена"


@app.errorhandler(400)
def error_400(error):
    return "Возможно, проблема в json запросе"


if __name__ == '__main__':
    app.run(debug=True, port=8000)
