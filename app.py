from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # SQLite база данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()

# Главная страница
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Проверка на уникальность
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует.', 'error')
            return redirect(url_for('signup'))

        # Хэширование пароля
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Сохранение в базу данных
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно! Войдите в свой аккаунт.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Поиск пользователя по email
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('profile'))  # Перенаправление на защищенную страницу
        else:
            flash(
                'Неправильный email или пароль. <a href="/signup">Зарегистрироваться?</a>',
                'error'
            )

    return render_template('login.html')


# Страница поиска
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        destination = request.form['destination']
        max_price = request.form['max_price']
        # Логика обработки запроса
        results = [
            {"price": 4500, "link": "http://example.com/ticket1"},
            {"price": 5000, "link": "http://example.com/ticket2"}
        ]
        return render_template('main.html', results=results)
    return render_template('main.html', results=[])

if __name__ == "__main__":
    app.run(debug=True)
