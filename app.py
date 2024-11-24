from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

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

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Получение данных из формы
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Простейшая валидация
        if not username or not email or not password:
            flash("Все поля обязательны для заполнения!", "error")
            return render_template('registration.html')
        if password != confirm_password:
            flash("Пароли не совпадают!", "error")
            return render_template('registration.html')

        # Логика добавления пользователя в базу данных (если используете базу)
        # new_user = User(username=username, email=email, password=generate_password_hash(password))
        # db.session.add(new_user)
        # db.session.commit()

        flash("Регистрация прошла успешно!", "success")

        # Перенаправление на страницу входа (или другую)
        return redirect(url_for('login'))  # Переход на страницу входа, например.

    return render_template('registration.html')

# Страница входа (пример)
@app.route('/login')
def login():
    return render_template('login.html')  # Отображение страницы входа

if __name__ == "__main__":
    app.run(debug=True)
