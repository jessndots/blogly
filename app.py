"""Blogly application."""

from flask import Flask, request, render_template, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
def new_user():
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


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('new-post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user.id)

    db.session.add(post)
    db.session.commit()

    flash(f'Post created for {user.first_name} {user.last_name}.')

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template('post-detail.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template('edit-post.html', user=user, post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    title = request.form['title']
    post.title = title

    content = request.form['content']
    post.content = content

    db.session.add(post)
    db.session.commit()

    flash(f'Post was edited.')   

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)  

    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    flash(f'Post was deleted.') 

    return redirect(f'/users/{user.id}')








