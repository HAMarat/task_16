from config import db
from models import User, Order, Offer

User(
    id=row.get("id"),
    first_name=row.get("first_name"),
    last_name=row.get("last_name"),
    age=row.get("age"),
    email=row.get("email"),
    role=row.get("role"),
    phone=row.get("phone")
)