@echo off
echo Запуск Django сервера...
echo.
echo Активируем виртуальное окружение...
call ..\.venv\Scripts\activate.bat
echo.
echo Проверяем Django проект...
python manage.py check
echo.
echo Применяем миграции...
python manage.py migrate
echo.
echo Запускаем сервер разработки...
echo Сайт будет доступен по адресу: http://127.0.0.1:8000/
echo.
python manage.py runserver
pause
