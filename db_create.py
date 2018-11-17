from application import db
from application.models import Transaction, Card


db.create_all()

print("DB created.")
