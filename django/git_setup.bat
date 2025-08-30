@echo off
echo Настройка Git репозитория для Django проекта...
echo.

echo 1. Добавляем все файлы в Git...
git add .

echo.
echo 2. Проверяем статус...
git status

echo.
echo 3. Создаем первый коммит...
git commit -m "Initial commit: Django website with Bootstrap and includes"

echo.
echo 4. Настраиваем пользователя Git (если нужно)...
git config user.name "valeri580"
git config user.email "valeri580@users.noreply.github.com"

echo.
echo 5. Создаем основную ветку...
git branch -M main

echo.
echo Git репозиторий готов!
echo.
echo Следующие шаги:
echo 1. Создайте новый репозиторий на GitHub: https://github.com/new
echo 2. Назовите его: django-bootstrap-website
echo 3. Выполните команды:
echo    git remote add origin https://github.com/valeri580/django-bootstrap-website.git
echo    git push -u origin main
echo.
pause
