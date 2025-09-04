@echo off
echo Скачивание портативной версии FFmpeg...
echo.

if not exist "ffmpeg_portable" mkdir ffmpeg_portable
cd ffmpeg_portable

echo Скачиваем FFmpeg...
curl -L "https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.1-essentials_build.zip" -o ffmpeg.zip

if exist "ffmpeg.zip" (
    echo Извлекаем архив...
    powershell -command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force"
    
    echo Настраиваем файлы...
    for /d %%i in (ffmpeg-*) do (
        copy "%%i\bin\ffmpeg.exe" .
        copy "%%i\bin\ffprobe.exe" .
        rmdir /s /q "%%i"
    )
    
    del ffmpeg.zip
    echo.
    echo FFmpeg установлен в папку ffmpeg_portable
    echo Для использования добавьте путь в код или PATH
    
    ffmpeg.exe -version
) else (
    echo Ошибка скачивания. Скачайте вручную с https://ffmpeg.org/download.html#build-windows
)

pause
