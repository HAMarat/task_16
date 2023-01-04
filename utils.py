import json
from config import db, app
from models import User, Offer, Order


def get_json_data(link):
    with open(link, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def serialize_user(row):
    return User(
        id=row.get("id"),
        first_name=row.get("first_name"),
        last_name=row.get("last_name"),
        age=row.get("age"),
        email=row.get("email"),
        role=row.get("role"),
        phone=row.get("phone")
    )


def serialize_order(row):
    return Order(
        id=row.get("id"),
        name=row.get("name"),
        description=row.get("description"),
        start_date=row.get("start_date"),
        end_date=row.get("end_date"),
        address=row.get("address"),
        price=row.get("price"),
        customer_id=row.get("customer_id"),
        executor_id=row.get("executor_id")
    )


def serialize_offer(row):
    return Offer(
        id=row.get("id"),
        order_id=row.get("order_id"),
        executor_id=row.get("executor_id")
    )


def add_data_to_user():
    for row in get_json_data('data/Users.json'):
        with app.app_context():
            db.session.add(serialize_user(row))
            db.session.commit()


def add_data_to_order():
    for row in get_json_data('data/Orders.json'):
        with app.app_context():
            db.session.add(serialize_order(row))
            db.session.commit()


def add_data_to_offer():
    for row in get_json_data('data/Offers.json'):
        with app.app_context():
            db.session.add(serialize_offer(row))
            db.session.commit()
