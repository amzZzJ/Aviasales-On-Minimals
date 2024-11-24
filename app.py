from flask import Flask, render_template, request

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
        max_price = float(request.form['max_price'])  # Преобразуем цену в число

        # Логика обработки запроса
        all_results = [
            {"price": 4500, "link": "http://example.com/ticket1"},
            {"price": 5000, "link": "http://example.com/ticket2"},
            {"price": 6000, "link": "http://example.com/ticket3"}
        ]

        # Фильтруем результаты по максимальной цене
        results = [result for result in all_results if result["price"] <= max_price]

        return render_template('main.html', results=results)

    return render_template('main.html', results=[])


if __name__ == "__main__":
    app.run(debug=True)
