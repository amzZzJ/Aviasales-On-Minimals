from src.app import app, db, User
import unittest
from unittest.mock import patch, MagicMock

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

    class SearchTestCase(unittest.TestCase):
        @patch('app.search_tickets')
        def test_search_success(self, mock_search):
            mock_search.return_value = [{
                'segments': [{'Вылет': 'Москва', 'Прилет': 'Санкт-Петербург', 'Перевозчик': 'Аэрофлот', 'Рейс': 'SU123',
                              'Самолет': 'Boeing 737'}],
                'Цена': '10 000',
                'Доступные места': '10'
            }]

            with app.test_client() as client:
                response = client.post('/search', data={
                    'from': 'Москва',
                    'to': 'Санкт-Петербург',
                    'date_from': '2024-12-01',
                    'date_to': '2024-12-10',
                    'max_price': '10000'
                })

                self.assertEqual(response.status_code, 200)
                self.assertIn('10 000', response.data.decode())


        @patch('app.search_tickets')
        def test_search_error(self, mock_search):
            mock_search.side_effect = Exception("Ошибка при парсинге")

            with app.test_client() as client:
                response = client.post('/search', data={
                    'from': 'Москва',
                    'to': 'Санкт-Петербург',
                    'date_from': '2024-12-01',
                    'date_to': '2024-12-10',
                    'max_price': '10000'
                })

                self.assertEqual(response.status_code, 200)

                self.assertIn('Ничего не найдено', response.data.decode())

if __name__ == '__main__':
    unittest.main()


