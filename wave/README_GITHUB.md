# 🎵 Wave - Терминальный аудио-помощник

Мощный инструмент командной строки для работы с аудио: синтез речи (TTS), транскрибация и классификация аудио.

## 🚀 Возможности

- 🎤 **TTS (Text-to-Speech)**: Озвучка текста через OpenAI API
- 📝 **Транскрибация**: Преобразование речи в текст с поддержкой больших файлов
- 🔊 **Классификация аудио**: Определение типа аудио (музыка/речь/шум) с помощью YamNet
- 📊 **Отчёты**: Генерация HTML и Word отчётов
- 📄 **Word экспорт**: Создание красиво оформленных документов
- 🎵 **Поддержка форматов**: WAV, MP3, M4A, FLAC, OGG

## 📋 Требования

- Python 3.9+
- FFmpeg (для обработки аудио)
- OpenAI API ключ
- Hugging Face API токен

## ⚡ Быстрая установка

### 1. Клонирование репозитория
```bash
git clone <your-repo-url>
cd wave
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Установка FFmpeg
**Windows:**
- Скачайте с https://ffmpeg.org/download.html
- Добавьте в PATH или поместите в `C:\ffmpeg\`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 5. Настройка API ключей
```bash
# Скопируйте шаблон
cp env_template.txt .env

# Отредактируйте .env файл и добавьте ваши ключи:
# OPENAI_API_KEY=sk-your-key-here
# HF_API_TOKEN=hf_your-token-here
```

## 🎯 Использование

### Синтез речи
```bash
python main.py tts "Ваш текст здесь" --voice alloy --out audio.mp3
```

### Транскрибация (с автоматической разбивкой больших файлов)
```bash
# Обычная транскрибация
python main.py transcribe audio.mp3 --out transcript.txt

# С созданием Word документа
python main.py transcribe audio.mp3 --out transcript.txt --word

# Большие файлы разбиваются автоматически
python main.py transcribe large_file.mp3 --out result.txt --word
```

### Классификация аудио
```bash
python main.py classify audio_folder/ --recurse
```

### Создание Word документа из текста
```bash
python main.py to-word transcript.txt --title "Мой документ"
```

### Копирование аудио в проект
```bash
python main.py ingest /path/to/audio --recurse
```

### HTML отчёты
```bash
python main.py report --html reports/analysis.html
```

## 🎨 Доступные голоса TTS

- `alloy` - универсальный
- `echo` - мужской
- `fable` - британский акцент  
- `onyx` - глубокий мужской
- `nova` - женский
- `shimmer` - мягкий женский

## 📁 Структура проекта

```
wave/
├── main.py              # Основной скрипт
├── requirements.txt     # Зависимости Python
├── env_template.txt     # Шаблон переменных окружения
├── .gitignore          # Исключения для Git
├── README.md           # Документация
├── data/               # Входные аудио файлы (игнорируется Git)
├── out/                # Выходные файлы (игнорируется Git)
└── reports/            # HTML отчёты (игнорируется Git)
```

## 🔧 Особенности

### Автоматическая разбивка больших файлов
Программа автоматически разбивает файлы больше 20 МБ на части по 10 минут, обрабатывает каждую часть отдельно и собирает результат.

### Поддержка русского языка
Отличное распознавание русской речи благодаря OpenAI Whisper.

### Интеллектуальный поиск FFmpeg
Программа автоматически находит FFmpeg в системе или в локальной папке.

## 💰 Примерная стоимость API

- **OpenAI TTS**: ~$0.015 за 1000 символов
- **OpenAI Whisper**: ~$0.006 за минуту аудио  
- **Hugging Face**: Бесплатно (с лимитами)

## 🛡️ Безопасность

- API ключи хранятся в `.env` файле (исключён из Git)
- Все конфиденциальные данные в `.gitignore`
- Локальная обработка данных

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект использует внешние API сервисы. Убедитесь, что у вас есть соответствующие права на использование OpenAI и Hugging Face API.

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте, что FFmpeg установлен
2. Убедитесь, что API ключи корректны
3. Проверьте подключение к интернету
4. Создайте Issue в репозитории

---

**Создано с ❤️ для работы с аудио контентом**
