import unittest
from app import app, db, User

class UserRegistrationTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user.db'
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration_success(self):
        response = self.client.post('/signup', data=dict(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        ), follow_redirects=True)

        self.assertIn('Регистрация прошла успешно! Войдите в свой аккаунт.', response.data.decode('utf-8'))

        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')

    def test_registration_existing_email(self):
        with app.app_context():
            user = User(username='testuser', email='test@example.com', password='testpassword')
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/signup', data=dict(
            username='newuser',
            email='test@example.com',
            password='newpassword'
        ), follow_redirects=True)

        self.assertIn('Пользователь с таким email уже существует.', response.data.decode('utf-8'))

    def test_registration_missing_fields(self):
        response = self.client.post('/signup', data=dict(
            username='',
            email='',
            password=''
        ), follow_redirects=True)

        self.assertIn('Все поля обязательны для заполнения!', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
