# Терминальный аудио-помощник

Мощный инструмент командной строки для работы с аудио: синтез речи (TTS), классификация аудио и транскрибация.

## Возможности

- 🎤 **TTS (Text-to-Speech)**: Озвучка текста через OpenAI API
- 🔊 **Классификация аудио**: Определение типа аудио (музыка/речь/шум) с помощью YamNet
- 📝 **Транскрибация**: Преобразование речи в текст через OpenAI Whisper
- 📊 **Отчёты**: Генерация HTML отчётов с результатами анализа
- 🎵 **Поддержка форматов**: WAV, MP3, M4A, FLAC, OGG

## Установка

### 1. Клонирование и переход в директорию
```bash
cd wave
```

### 2. Создание виртуального окружения (рекомендуется)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Установка FFmpeg (требуется для обработки аудио)
**Windows:**
- Скачайте FFmpeg с https://ffmpeg.org/download.html
- Добавьте путь к FFmpeg в PATH

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 5. Настройка API ключей
1. Скопируйте `env_template.txt` в `.env`:
```bash
copy env_template.txt .env  # Windows
cp env_template.txt .env    # Linux/macOS
```

2. Отредактируйте `.env` файл и добавьте ваши API ключи:
   - **OpenAI API ключ**: Получите на https://platform.openai.com/api-keys
   - **Hugging Face токен**: Получите на https://huggingface.co/settings/tokens

## Использование

### Базовые команды

```bash
# Помощь по всем командам
python main.py --help

# TTS - озвучка текста
python main.py tts "Привет, это тест синтеза речи" --voice alloy --out output.mp3

# Транскрибация аудио
python main.py transcribe audio.wav --out transcript.txt

# Классификация аудио файлов
python main.py classify audio_folder/ --recurse

# Генерация отчёта
python main.py report --html reports/audio_report.html

# Копирование аудио файлов в рабочую директорию
python main.py ingest /path/to/audio/files --recurse
```

### Примеры использования

#### 1. Анализ папки с аудио
```bash
# Классифицировать все аудио файлы в папке
python main.py classify ./audio_samples --recurse

# Создать HTML отчёт
python main.py report --html reports/analysis.html
```

#### 2. Создание аудио из текста
```bash
# Озвучить текст голосом "nova"
python main.py tts "Добро пожаловать в наш сервис" --voice nova --out welcome.mp3
```

#### 3. Транскрибация интервью
```bash
# Преобразовать речь в текст с контекстом
python main.py transcribe interview.wav --prompt "Интервью с экспертом по AI" --out interview.txt
```

## Структура проекта

```
wave/
├── main.py              # Основной скрипт
├── requirements.txt     # Зависимости Python
├── env_template.txt     # Шаблон для переменных окружения
├── README.md           # Документация
├── data/               # Входные аудио файлы
├── out/                # Выходные файлы и промежуточные результаты
└── reports/            # HTML отчёты
```

## Поддерживаемые голоса TTS

- `alloy` - Универсальный голос
- `echo` - Мужской голос
- `fable` - Британский акцент
- `onyx` - Глубокий мужской голос
- `nova` - Женский голос
- `shimmer` - Мягкий женский голос

## Поддерживаемые форматы аудио

**Входные форматы**: WAV, MP3, M4A, FLAC, OGG
**Выходные форматы**: MP3, WAV

## Устранение неполадок

### Ошибка "FFmpeg not found"
Убедитесь, что FFmpeg установлен и доступен в PATH.

### Ошибка API ключей
Проверьте правильность API ключей в `.env` файле и наличие средств на счетах OpenAI/Hugging Face.

### Ошибки при классификации
Убедитесь, что Hugging Face токен имеет права на использование Inference API.

## Лицензия

Этот проект использует внешние API сервисы:
- OpenAI API (платный)
- Hugging Face Inference API (бесплатный уровень доступен)

Убедитесь, что у вас есть соответствующие лицензии и квоты для использования этих сервисов.
