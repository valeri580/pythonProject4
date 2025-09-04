@echo off
echo ========================================
echo Подготовка проекта Wave для GitHub
echo ========================================
echo.

echo 1. Проверка конфиденциальных файлов...
if exist .env (
    echo [ВНИМАНИЕ] Найден файл .env - он будет исключен из Git
    echo Содержимое .env НЕ будет загружено в GitHub ✓
) else (
    echo .env файл не найден ✓
)

echo.
echo 2. Очистка временных файлов...
if exist data rmdir /s /q data 2>nul
if exist out rmdir /s /q out 2>nul
if exist reports rmdir /s /q reports 2>nul
del *.mp3 2>nul
del *.wav 2>nul
del *.docx 2>nul
del transcript_* 2>nul
del *_test* 2>nul
del final_test* 2>nul
echo Временные файлы очищены ✓

echo.
echo 3. Создание необходимых папок...
mkdir data 2>nul
mkdir out 2>nul
mkdir reports 2>nul
echo Структура папок создана ✓

echo.
echo 4. Проверка .gitignore...
if exist .gitignore (
    echo .gitignore файл существует ✓
) else (
    echo [ОШИБКА] .gitignore не найден!
)

echo.
echo 5. Проверка README...
if exist README_GITHUB.md (
    echo README_GITHUB.md готов ✓
    echo Переименуйте его в README.md перед загрузкой
) else (
    echo [ОШИБКА] README_GITHUB.md не найден!
)

echo.
echo 6. Проверка requirements.txt...
if exist requirements.txt (
    echo requirements.txt готов ✓
) else (
    echo [ОШИБКА] requirements.txt не найден!
)

echo.
echo 7. Проверка шаблона окружения...
if exist env_template.txt (
    echo env_template.txt готов ✓
) else (
    echo [ОШИБКА] env_template.txt не найден!
)

echo.
echo ========================================
echo ПРОЕКТ ГОТОВ К ЗАГРУЗКЕ В GITHUB!
echo ========================================
echo.
echo Следующие шаги:
echo 1. git init
echo 2. git add .
echo 3. git commit -m "Initial commit: Wave audio assistant"
echo 4. git remote add origin https://github.com/username/wave.git
echo 5. git push -u origin main
echo.
echo ВАЖНО: API ключи НЕ будут загружены благодаря .gitignore
echo.
pause
