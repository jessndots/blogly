from app import app
from models import db, User
from unittest import TestCase

app.config['TESTING']=True 
app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserRoutesTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        test_user = User(first_name='test', last_name='user', image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn("<button><a href=\'/users/add\'>Add User</a></button>", html)

    
    def test_add_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/add')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="first_name">First Name</label>', html)
            self.assertIn('<input type="text" id=\'image_url\' name="image_url">', html)
            self.assertIn('<button>Add</button>', html)

    def test_add_user_submit(self):
        with app.test_client() as client:
            resp = client.post('/users/add', data={'first_name': 'first', 'last_name': 'last', 'image_url': ''})
            user = User.query.filter_by(first_name = 'first')[0]
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'http://localhost/users/{user.id}')

    def test_add_user_redirection(self):
        with app.test_client() as client:
            resp = client.post('/users/add', data = {'first_name': 'first', 'last_name':'last', 'image_url': ''}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('first last', html)

    def test_show_user(self):
        with app.test_client() as client:
            user = User.query.first()
            resp = client.get(f'/users/{user.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{user.first_name} {user.last_name}</h1>', html)
            self.assertIn(f'<button><a href="/users/{user.id}/delete">Delete</a></button>', html)

    def test_edit_user_form(self):
        with app.test_client() as client:
            user = User.query.first()
            resp = client.get(f'/users/{user.id}/edit')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit User</h1>', html)
            self.assertIn('<label for="last_name">Last Name</label>', html)
            self.assertIn(f'<button><a href="/users/{user.id}">Cancel</a></button>', html)

    def test_edit_user_submit(self):
        with app.test_client() as client:
            user = User.query.first()
            resp = client.post(f'/users/{user.id}/edit', data = {'first_name': 'first2', 'last_name': 'last2', 'image_url': 'https://synapse.it/wp-content/uploads/2020/12/test-600x600.png'})
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'http://localhost/users/{user.id}')

    def test_edit_user_redirection(self):
        with app.test_client() as client:
            user = User.query.first()
            resp = client.post(f'/users/{user.id}/edit', data = {'first_name': 'first2', 'last_name': 'last2', 'image_url': 'https://synapse.it/wp-content/uploads/2020/12/test-600x600.png'}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>first2 last2</h1>', html)
            self.assertIn(f'<button><a href="/users/{user.id}/delete">Delete</a></button>', html)
            self.assertIn(f'<img src="https://synapse.it/wp-content/uploads/2020/12/test-600x600.png">', html)

    def test_delete_user(self):
        with app.test_client() as client:
            user = User.query.first()
            resp = client.get(f'/users/{user.id}/delete')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)

    def test_delete_user_redirection(self):
        with app.test_client() as client:
            user = User.query.first()
            resp = client.get(f'/users/{user.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn(f'User {user.first_name} {user.last_name} was deleted.', html)
            self.assertNotIn(f'{user.first_name} {user.last_name}</a></li>', html)