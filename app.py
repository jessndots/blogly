"""Blogly application."""

from flask import Flask, request, render_template, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug=DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True




connect_db(app)

@app.route('/')
def redirect_users():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/add')
def add_user_form():
    
    return render_template('add-user.html')


@app.route('/users/add', methods=['POST'])
def add_user():
    first = request.form['first_name']
    last = request.form['last_name']

    user = User(first_name=first, last_name=last)

    if request.form['image_url'] is not "":
        user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    
    flash(f'User {user.first_name} {user.last_name} was added.')   

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    first = request.form['first_name']
    if first is not "":
        user.first_name = first
    
    last = request.form['last_name']
    if last is not "":
        user.last_name = last
    
    img = request.form['image_url'] 
    if img is not "":
        user.image_url = img

    db.session.add(user)
    db.session.commit()

    flash(f'User {user.first_name} {user.last_name} was edited.')   

    return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    flash(f'User {user.first_name} {user.last_name} was deleted.')    
    User.query.filter(User.id == user_id).delete()

    db.session.commit()
    return redirect('/users')