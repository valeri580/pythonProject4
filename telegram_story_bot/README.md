# Telegram Story Bot

Телеграм бот для автоматического размещения сторис в Telegram пользователя.

## Возможности

- 🔹 Автоматическое размещение сторис по расписанию
- 🔹 Получение контента из XML фида
- 🔹 Настраиваемые шаблоны для заголовков и текста
- 🔹 Управление через команды: старт / стоп / статус
- 🔹 Поддержка множественных аккаунтов
- 🔹 Логирование всех операций

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте конфигурацию в файле `config.ini`

3. Запустите бота:
```bash
python telegram_story_bot.py
```

## Конфигурация

### Основные настройки (DEFAULT)
- `bot_token` - токен вашего Telegram бота
- `acccount` - ID аккаунтов для размещения сторис (через запятую)
- `admins` - ID администраторов (через запятую)

### Настройки контента (CONTENT)
- `URL` - URL XML фида
- `storys_time` - время размещения сторис (формат HH:MM, через запятую)
- `storys_days` - дни недели для размещения (* для всех дней)
- `title` - шаблон заголовка сторис
- `text` - шаблон текста сторис

## Использование

### CLI команды
- `start` - запуск бота
- `stop` - остановка бота
- `status` - просмотр статуса
- `exit` - выход из программы

### Шаблоны текста
Используйте поля из фида в кавычках:
- `"category" "модель", "год выпуска"` → Audi Q3 Sportback, 2025
- `"category" "модель", "год выпуска" год. Цена "price" "currencyId"` → Audi Q3 Sportback, 2025 год. Цена 4306730 RUR

## Деплой на VPS

### Ubuntu + Apache

1. Установите Python и зависимости:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

2. Скопируйте файлы проекта на сервер

3. Установите зависимости:
```bash
pip3 install -r requirements.txt
```

4. Настройте systemd сервис для автозапуска:
```bash
sudo nano /etc/systemd/system/telegram-story-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=Telegram Story Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/telegram_story_bot
ExecStart=/usr/bin/python3 telegram_story_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

5. Запустите сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-story-bot
sudo systemctl start telegram-story-bot
```

## Логи

Логи сохраняются в файл `bot.log` в папке проекта.

## Примечания

- Для размещения сторис требуется использовать MTProto API (не реализовано в текущей версии)
- Убедитесь, что у вас есть права на размещение контента в указанных аккаунтах
- Рекомендуется использовать виртуальное окружение Python

## Лицензия

MIT License
