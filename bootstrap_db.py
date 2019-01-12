from application import db
from application.models import Transaction, Card, School, User

# drops all tables
db.reflect()
db.drop_all()

# creates all tables
db.create_all()

# create schools
qkr_training_school = School(name='Qkr Training School')
westmead_school = School(name='Westmead School')
toongabie_school = School(name='Toongabie School')

db.session.add(qkr_training_school)
db.session.add(westmead_school)
db.session.add(toongabie_school)


# create users and associate schools
muhammad_ali = User(name='Suzy Chase', school=qkr_training_school, balance = 100.00)
akul = User(name='Akul', school=qkr_training_school, balance = 100.00)
dwij = User(name='Dwij', school=westmead_school, balance = 100.00)

db.session.add(muhammad_ali)
db.session.add(akul)
db.session.add(dwij)

db.session.commit()

# update school association of a user
toongabie_school = School.query.filter_by(name='Toongabie School').first()
akul=User.query.filter_by(name='Akul').first()
akul.school_id = toongabie_school.id
db.session.add(akul)
db.session.commit()

# create cards
apple_pay = Card(number='44196689710181', expiry_date='1219', owner_id=muhammad_ali.id)
twentyeight_degree_card = Card(number='54443453022605', expiry_date='1219', owner_id=muhammad_ali.id)
hsbc_card = Card(number='45859400111425', expiry_date='1219', owner_id=muhammad_ali.id)
card2 = Card(number='55554444333311', expiry_date='1219', owner_id=dwij.id)
card3 = Card(number='55554444333300', expiry_date='1219', owner_id=akul.id)
card4 = Card(number='55554444333333', expiry_date='1219', owner_id=muhammad_ali.id)
card5 = Card(number='55203800170812', expiry_date='1219', owner_id=muhammad_ali.id)
card6 = Card(number='047FFFFFFFA40A275EFF', expiry_date='1219', owner_id=muhammad_ali.id)
card7 = Card(number='04FFFFFFFDFFFFFFA50A', expiry_date='1219', owner_id=muhammad_ali.id)
db.session.add_all([apple_pay, twentyeight_degree_card, hsbc_card, card2, card3, card4, card5, card6, card7])
db.session.commit()

add_balance_transaction_1 = Transaction(card_num=apple_pay.number, type='ADD_BALANCE', amount=500.00, status='APPROVED')
add_balance_transaction_2 = Transaction(card_num=card2.number, type='ADD_BALANCE', amount=100.00, status='APPROVED')
add_balance_transaction_3 = Transaction(card_num=card3.number, type='ADD_BALANCE', amount=50.50, status='APPROVED')
check_balance_transaction = Transaction(card_num=card3.number, type='CHECK_BALANCE', status='APPROVED')

#db.session.add(add_balance_transaction_1)
#db.session.add(add_balance_transaction_2)
#db.session.add(add_balance_transaction_3)
#db.session.add(check_balance_transaction)
#db.session.commit()

