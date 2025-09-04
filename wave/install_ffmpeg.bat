@echo off
echo ========================================
echo Установка FFmpeg для Windows
echo ========================================
echo.

echo Создаем папку для FFmpeg...
if not exist "C:\ffmpeg" mkdir "C:\ffmpeg"
cd /d "C:\ffmpeg"

echo.
echo Скачиваем FFmpeg (это может занять несколько минут)...
echo URL: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'}"

if not exist "ffmpeg.zip" (
    echo ОШИБКА: Не удалось скачать FFmpeg
    echo Попробуйте скачать вручную с https://ffmpeg.org/download.html#build-windows
    pause
    exit /b 1
)

echo.
echo Извлекаем архив...
powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force"

echo.
echo Ищем папку с FFmpeg...
for /d %%i in (ffmpeg-*) do (
    echo Найдена папка: %%i
    move "%%i\bin\*" "."
    rmdir /s /q "%%i"
)

echo.
echo Очищаем временные файлы...
del ffmpeg.zip

echo.
echo Проверяем установку...
ffmpeg -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo Добавляем FFmpeg в PATH...
    echo Добавьте C:\ffmpeg в переменную PATH:
    echo 1. Нажмите Win+R, введите sysdm.cpl
    echo 2. Перейдите на вкладку "Дополнительно"
    echo 3. Нажмите "Переменные среды"
    echo 4. В разделе "Системные переменные" найдите PATH
    echo 5. Добавьте C:\ffmpeg
    echo 6. Перезапустите командную строку
    echo.
) else (
    echo ✓ FFmpeg успешно установлен!
)

echo.
echo Установка завершена!
echo FFmpeg установлен в: C:\ffmpeg
echo.
pause
