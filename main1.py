from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index2.html',
                         title="Главная страница",
                         welcome="Добро пожаловать на наш сайт!")

@app.route('/blog')
def blog():
    posts = [
        {"title": "Мой пост", "date": "12.08.2025", "content": "Сегодня я изучаю Flask и Jinja!"},
        {"title": "Второй пост", "date": "12.08.2025", "content": "Продолжаю изучение веб-разработки."}
    ]
    return render_template('home.html',
                         title="Блог",
                         posts=posts)

@app.route('/about')  # Маршрут /about
def about():
    about_info = {
        "email": "info@example.com",
        "phone": "+7 (123) 456-78-90",
        "address": "г. Москва, ул. Примерная, д. 1"
    }
    return render_template('about.html', title="Контакты", contacts=about_info)

if __name__ == '__main__':
    app.run(debug=True)