from models import User, Post, Tag, PostTag, db
from app import app


# create all tables
db.drop_all()
db.create_all()


# create users
u1 = User(first_name = 'Jessica', last_name='Doty')
u2 = User(first_name='Katy', last_name='Wright')

db.session.add(u1)
db.session.add(u2)

db.session.commit()



# create tags
t1 = Tag(name = 'tag 1')
t2 = Tag(name = 'tag 2')
t3 = Tag(name = 'tag 3')

db.session.add(t1)
db.session.add(t2)
db.session.add(t3)

db.session.commit()




# create posts
p1 = Post(title = 'title 1', content = 'content 1', user_id = u1.id)
p2 = Post(title = 'title 2', content = 'content 2', user_id = u2.id)

db.session.add(p1)
db.session.add(p2)

db.session.commit()