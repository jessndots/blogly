from typing import TYPE_CHECKING

import datetime

from sqlalchemy.orm import backref

if TYPE_CHECKING:
    from _typeshed import Self

from flask_sqlalchemy import SQLAlchemy
db= SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""
class User(db.Model): 
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    image_url = db.Column(db.String, default = "https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg")
    

    def __repr__(self): 
        """Show info about user."""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref = 'posts')
    
    def __repr__(self):
        """Show info about post."""
        p = self
        return f"<Post {p.id} {p.title} {p.created_at} {p.user_id} {p.tags}"

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")




class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False, unique = True)

    posts = db.relationship('Post', secondary = 'posts_tags', backref = 'tags')

    def __repr__(self):
        """Show info about tag."""
        t = self
        return f"<Tag {t.id} {t.name} {t.posts}>"


class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete='CASCADE'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete='CASCADE'), primary_key = True)
