from application import db
from application.models import Transaction, Card, School, User


db.create_all()

print("DB created.")
