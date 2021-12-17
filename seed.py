from models import User, connect_db, db
from app import app

# create all tables
db.drop_all()
db.create_all()

u1 = User(first_name = 'Jessica', last_name='Doty')
u2 = User(first_name='Katy', last_name='Wright')

db.session.add(u1)
db.session.add(u2)

db.session.commit()