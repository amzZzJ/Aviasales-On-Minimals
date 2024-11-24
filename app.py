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


if __name__ == "__main__":
    app.run(debug=True)
