import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from parsers.parser_aeroflot import search_tickets

app = Flask(__name__, template_folder='resources/templates')

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, 'resources', 'user.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'anyakseniaamina'

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

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/search', methods=['POST'])
def search():
    city_from = request.form['from']
    city_to = request.form['to']
    date_from = str(request.form['date_from'])
    date_to = str(request.form['date_to'])
    max_price = str(request.form['max_price'])

    try:
        results = search_tickets(
        city_from=city_from,
        city_to=city_to,
        date_from=date_from,
        date_to=date_to)

        for result in results:
            result['segments'] = [
                segment for segment in result['segments']
                if segment['Вылет'] not in ['ЛУЧШАЯ ЦЕНА', 'В ПУТИ', 'Пересадка']
            ]

        #print("Результаты: ", results)
    except Exception as e:
        results = []
        print(f"Ошибка при парсинге: {e}")

    return render_template('results.html', results=results)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Сначала войдите в аккаунт.', 'error')
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('Все поля обязательны для заполнения!', 'error')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует.', 'error')
            return redirect(url_for('signup'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

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

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('profile'))
        else:
            flash(
                'Неправильный email или пароль. <a href="/signup">Зарегистрироваться?</a>',
                'error'
            )

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из аккаунта.', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
