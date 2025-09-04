@echo off
echo Настройка окружения для аудио-помощника wave
echo ============================================

echo.
echo 1. Проверка Python...
python --version
if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: Python не найден. Установите Python 3.9+ и добавьте в PATH
    pause
    exit /b 1
)

echo.
echo 2. Создание виртуального окружения...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo ОШИБКА: Не удалось создать виртуальное окружение
    pause
    exit /b 1
)

echo.
echo 3. Активация виртуального окружения...
call venv\Scripts\activate.bat

echo.
echo 4. Обновление pip...
python -m pip install --upgrade pip

echo.
echo 5. Установка зависимостей...
pip install typer==0.9.0 rich==13.7.1 python-dotenv httpx openai click==8.1.7

echo.
echo 6. Проверка FFmpeg...
ffmpeg -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ПРЕДУПРЕЖДЕНИЕ: FFmpeg не найден. Скачайте с https://ffmpeg.org/download.html
    echo и добавьте в PATH для работы с аудио файлами
) else (
    echo FFmpeg найден ✓
)

echo.
echo 7. Создание .env файла...
if not exist .env (
    copy env_template.txt .env
    echo Создан файл .env. Отредактируйте его и добавьте ваши API ключи:
    echo - OPENAI_API_KEY (получить на https://platform.openai.com/api-keys)
    echo - HF_API_TOKEN (получить на https://huggingface.co/settings/tokens)
) else (
    echo Файл .env уже существует
)

echo.
echo 8. Тестирование приложения...
python main.py --help
if %ERRORLEVEL% neq 0 (
    echo ПРЕДУПРЕЖДЕНИЕ: Есть проблемы с запуском приложения
) else (
    echo Приложение готово к работе ✓
)

echo.
echo Настройка завершена!
echo Для запуска приложения используйте: python main.py [команда]
echo Список команд: python main.py --help
pause
