import sqlalchemy
from flask import jsonify, request
from utils import add_data_to_user, add_data_to_order, add_data_to_offer, serialize_user, \
    serialize_order, serialize_offer
from config import app, db
from models import User, Order, Offer

# удаляем ранее созданные таблицы и создаем необходимые
with app.app_context():
    db.drop_all()
    db.create_all()

# Заполняем таблица данными из json файлов
add_data_to_user()
add_data_to_order()
add_data_to_offer()


@app.route('/users', methods=['GET', 'POST'])
def return_users():
    """
    Вьюшка для возвращения всех данных из таблицы User по GET запросу или добавления новой строки по POST запросу
    """
    if request.method == 'GET':
        result = []
        users = db.session.query(User).all()
        for user in users:
            result.append(user.get_dict_user())
        return jsonify(result)

    elif request.method == 'POST':
        try:
            db.session.add(serialize_user(request.json))
            db.session.commit()
        # Обработка исключения при попытке добавления записи с не уникальным primary key
        except sqlalchemy.exc.IntegrityError as error:
            return f'{error}'
        return jsonify(code=200)

    return f"запрос не обработан"


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def return_user_by_id(user_id):
    """
    Вьюшка для возвращения данных одной строки из таблицы User по GET запросу, обновления строки по PUT запросу
    или удаления строки по запросу DELETE
    """
    if request.method == 'GET':
        user = db.session.query(User).get(user_id)
        if user:
            return jsonify(user.get_dict_user())
        return f"Пользователь с id {user_id} не найден"

    elif request.method == 'PUT':
        user = db.session.query(User).get(user_id)
        if user:
            try:
                db.session.query(User).filter(User.id == user_id).update(request.json)
                db.session.commit()
                return jsonify(code=200)
            # Обработка исключения при попытке добавления записи с не уникальным primary key
            except sqlalchemy.exc.IntegrityError as error:
                return f'{error}'
            # Обработка исключения при попытке обновления записи с не несоответствующими столбцами
            except sqlalchemy.exc.InvalidRequestError as error:
                return f'{error}'
        return f"Пользователь с id {user_id} не найден"

    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(code=200)
        return f"Пользователь с id {user_id} не найден"

    return f"запрос не обработан"


@app.route('/orders', methods=['GET', 'POST'])
def return_orders():
    """
    Вьюшка для возвращения всех данных из таблицы Order по GET запросу или добавления новой строки по POST запросу
    """
    if request.method == 'GET':
        result = []
        orders = db.session.query(Order).all()
        for order in orders:
            result.append(order.get_dict_order())
        return jsonify(result)

    elif request.method == 'POST':
        # Обработка исключения при попытке добавления записи с не уникальным primary key
        try:
            db.session.add(serialize_order(request.json))
            db.session.commit()
        # Обработка исключения при попытке добавления записи с не уникальным primary key
        except sqlalchemy.exc.IntegrityError as error:
            return f'{error}'
        return jsonify(code=200)

    return f"запрос не обработан"


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def return_order_by_id(order_id):
    """
    Вьюшка для возвращения данных одной строки из таблицы Order по GET запросу, обновления строки по PUT запросу
    или удаления строки по запросу DELETE
    """
    if request.method == 'GET':
        order = db.session.query(Order).get(order_id)
        if order:
            return jsonify(order.get_dict_order())
        return f"Пользователь с id {order_id} не найден"

    elif request.method == 'PUT':
        order = db.session.query(Order).get(order_id)
        if order:
            try:
                db.session.query(Order).filter(Order.id == order_id).update(request.json)
                db.session.commit()
                return jsonify(code=200)
            # Обработка исключения при попытке добавления записи с не уникальным primary key
            except sqlalchemy.exc.IntegrityError as error:
                return f'{error}'
            # Обработка исключения при попытке обновления записи с не несоответствующими столбцами
            except sqlalchemy.exc.InvalidRequestError as error:
                return f'{error}'
        return f"Пользователь с id {order_id} не найден"

    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return jsonify(code=200)
        return f"Пользователь с id {order_id} не найден"

    return f"запрос не обработан"


@app.route('/offers', methods=['GET', 'POST'])
def return_offers():
    """
    Вьюшка для возвращения всех данных из таблицы Offer по GET запросу или добавления новой строки по POST запросу
    """
    if request.method == 'GET':
        result = []
        offers = db.session.query(Offer).all()
        for offer in offers:
            result.append(offer.get_dict_offer())
        return jsonify(result)

    elif request.method == 'POST':
        try:
            db.session.add(serialize_offer(request.json))
            db.session.commit()
        # Обработка исключения при попытке добавления записи с не уникальным primary key
        except sqlalchemy.exc.IntegrityError as error:
            return f'{error}'
        return jsonify(code=200)

    return f"запрос не обработан"


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def return_offer_by_id(offer_id):
    """
    Вьюшка для возвращения данных одной строки из таблицы Offer по GET запросу, обновления строки по PUT запросу
    или удаления строки по запросу DELETE
    """
    if request.method == 'GET':
        offer = db.session.query(Offer).get(offer_id)
        if offer:
            return jsonify(offer.get_dict_offer())
        return f"Пользователь с id {offer_id} не найден"

    elif request.method == 'PUT':
        offer = db.session.query(Offer).get(offer_id)
        if offer:
            try:
                db.session.query(Offer).filter(Offer.id == offer_id).update(request.json)
                db.session.commit()
                return jsonify(code=200)
            # Обработка исключения при попытке добавления записи с не уникальным primary key
            except sqlalchemy.exc.IntegrityError as error:
                return f'{error}'
            # Обработка исключения при попытке обновления записи с не несоответствующими столбцами
            except sqlalchemy.exc.InvalidRequestError as error:
                return f'{error}'
        return f"Пользователь с id {offer_id} не найден"

    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        if offer:
            db.session.delete(offer)
            db.session.commit()
            return jsonify(code=200)
        return f"Пользователь с id {offer_id} не найден"

    return f"запрос не обработан"


@app.errorhandler(404)
def error_404(error):
    """
    Вьюшка для обработки не найденной страницы
    """
    return f"Страница не найдена. Ошибка: {error}", 404


@app.errorhandler(400)
def error_400(error):
    """
    Вьюшка для обработки при не корректном json запросе
    """
    return f"Возможно, проблема в json запросе. Ошибка: {error}", 400


if __name__ == '__main__':
    app.run(port=8000)
