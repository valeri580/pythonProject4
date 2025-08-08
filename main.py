from flask import Flask, render_template, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)


@app.route('/')
def show_current_time():
    # Получаем текущие дату и время
    current_time = datetime.now()

    # Форматируем дату и время для красивого отображения
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Передаем время в шаблон
    return render_template('index.html', current_time=formatted_time)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/image'),
                             'icons_favicon.png',
                             mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)