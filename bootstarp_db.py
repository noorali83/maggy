from application import db
from application.models import Transaction, Card, School, User

# drops all tables
db.reflect()
db.drop_all()

# creates all tables
db.create_all()

# create schools
darcy_road_school = School(name='Darcy Road School')
westmead_school = School(name='Westmead School')
toongabie_school = School(name='Toongabie School')

db.session.add(darcy_road_school)
db.session.add(westmead_school)
db.session.add(toongabie_school)


# create users and associate schools
muhammad_ali = User(name='Muhammad Ali', school=darcy_road_school)
akul = User(name='Akul', school=darcy_road_school)
dwij = User(name='Dwij', school=westmead_school)

db.session.add(muhammad_ali)
db.session.add(akul)
db.session.add(dwij)

db.session.commit()

# update school association of a user
toongabie_school=School.query.filter_by(name='Toongabie School').first()
akul=User.query.filter_by(name='Akul').first()
akul.school_id = toongabie_school.id
db.session.add(akul)
db.session.commit()

# create cards
card1 = Card(number='5555444433332222', expiry_date='1219',owner_id=muhammad_ali.id)
card2 = Card(number='5555444433331111', expiry_date='1219',owner_id=dwij.id)
card3 = Card(number='5555444433330000', expiry_date='1219',owner_id=akul.id)
db.session.add(card1)
db.session.add(card2)
db.session.add(card3)
db.session.commit()

add_balance_transaction_1=Transaction(card_num=card1.number, type='ADD_BALANCE', amount=500.00, status='APPROVED')
add_balance_transaction_2=Transaction(card_num=card2.number, type='ADD_BALANCE', amount=100.00, status='APPROVED')
add_balance_transaction_3=Transaction(card_num=card3.number, type='ADD_BALANCE', amount=50.50, status='APPROVED')
check_balance_transaction=Transaction(card_num=card3.number, type='CHECK_BALANCE', status='APPROVED')

db.session.add(add_balance_transaction_1)
db.session.add(add_balance_transaction_2)
db.session.add(add_balance_transaction_3)
db.session.add(check_balance_transaction)
db.session.commit()

