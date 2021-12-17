from typing import TYPE_CHECKING

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