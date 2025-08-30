# 🚀 Быстрый старт - Telegram Story Bot

## Установка и запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации
Отредактируйте файл `config.ini`:
- Замените `bot_token` на ваш токен бота
- Укажите ваши ID в `admins` и `acccount`
- Настройте URL фида и время размещения

### 3. Запуск

#### Вариант 1: CLI интерфейс
```bash
python telegram_story_bot.py
```
Команды: `start`, `stop`, `status`, `exit`

#### Вариант 2: Веб-интерфейс
```bash
python web_interface.py
```
Откройте http://localhost:5000

#### Вариант 3: Telegram бот управления
```bash
python telegram_control_bot.py
```
Используйте команды в Telegram: `/start`, `/status`, `/start_bot`, `/stop_bot`

## Деплой на VPS

### Автоматический деплой
```bash
chmod +x deploy.sh
sudo ./deploy.sh
```

### Ручной деплой
1. Скопируйте файлы на сервер
2. Установите зависимости: `pip3 install -r requirements.txt`
3. Настройте systemd сервис: `sudo cp telegram-story-bot.service /etc/systemd/system/`
4. Запустите: `sudo systemctl start telegram-story-bot`

## Полезные команды

### Управление сервисом
```bash
sudo systemctl status telegram-story-bot
sudo systemctl start telegram-story-bot
sudo systemctl stop telegram-story-bot
sudo systemctl restart telegram-story-bot
```

### Просмотр логов
```bash
journalctl -u telegram-story-bot -f
tail -f bot.log
```

## Структура проекта

```
telegram_story_bot/
├── telegram_story_bot.py      # Основной бот
├── telegram_control_bot.py    # Telegram бот управления
├── web_interface.py          # Веб-интерфейс
├── config.ini               # Конфигурация
├── requirements.txt         # Зависимости
├── deploy.sh               # Скрипт деплоя
├── telegram-story-bot.service # Systemd сервис
├── README.md               # Документация
├── QUICK_START.md          # Этот файл
└── .gitignore              # Исключения Git
```

## Примечания

⚠️ **Важно:** Для размещения сторис требуется реализация MTProto API (не включено в текущую версию)

🔧 **Настройка:** Все настройки в файле `config.ini`

📝 **Логи:** Сохраняются в `bot.log` и через systemd

🌐 **Веб-интерфейс:** Доступен на порту 5000
