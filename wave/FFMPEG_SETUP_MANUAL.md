# 🔧 Ручная установка FFmpeg (из-за проблем с кодировкой PowerShell)

## 📥 Быстрая установка

### Вариант 1: Скачать готовый FFmpeg
1. Откройте браузер и перейдите на: https://www.gyan.dev/ffmpeg/builds/
2. Скачайте файл: **ffmpeg-release-essentials.zip** (~100 МБ)
3. Создайте папку `C:\ffmpeg`
4. Извлеките архив в эту папку
5. Добавьте `C:\ffmpeg\bin` в PATH (см. инструкцию ниже)

### Вариант 2: Портативная версия в проекте
1. Создайте папку `ffmpeg_portable` в папке wave
2. Скачайте https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.1-essentials_build.zip
3. Извлеките `ffmpeg.exe` в папку `ffmpeg_portable`
4. Приложение автоматически найдет FFmpeg в этой папке

### Вариант 3: Через winget (Windows 10/11)
Откройте PowerShell от администратора и выполните:
```
winget install ffmpeg
```

## 🔧 Добавление в PATH

1. Нажмите `Win + R`, введите `sysdm.cpl`
2. Перейдите на вкладку "Дополнительно"
3. Нажмите "Переменные среды"
4. В "Системные переменные" найдите `PATH`
5. Нажмите "Изменить" → "Создать"
6. Добавьте путь: `C:\ffmpeg\bin`
7. Нажмите "OK" везде
8. Перезапустите командную строку

## ✅ Проверка установки

```bash
ffmpeg -version
```

## 🧪 Тестирование с wave

После установки FFmpeg:

```bash
# Классификация аудио
python main.py classify out/tts_output.mp3

# Конвертация аудио
python main.py transcribe any_audio_file.wav
```

## 📝 Примечание

Приложение wave работает и без FFmpeg:
- ✅ TTS (синтез речи) - работает
- ✅ Транскрибация MP3/WAV - работает  
- ❌ Классификация аудио - требует FFmpeg
- ❌ Конвертация форматов - требует FFmpeg
