#!/bin/bash

# Скрипт для деплоя Telegram Story Bot на Ubuntu VPS
# Использование: ./deploy.sh

set -e

echo "🚀 Начинаем деплой Telegram Story Bot..."

# Проверяем, что мы root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Этот скрипт должен быть запущен от имени root"
    exit 1
fi

# Обновляем систему
echo "📦 Обновляем систему..."
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
echo "📦 Устанавливаем зависимости..."
apt install -y python3 python3-pip python3-venv apache2 git curl wget

# Создаем директорию для проекта
echo "📁 Создаем директорию проекта..."
mkdir -p /var/www/telegram_story_bot
chown www-data:www-data /var/www/telegram_story_bot

# Переходим в директорию проекта
cd /var/www/telegram_story_bot

# Создаем виртуальное окружение
echo "🐍 Создаем виртуальное окружение Python..."
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
echo "📦 Устанавливаем Python зависимости..."
pip install --upgrade pip
pip install -r requirements.txt

# Настраиваем права доступа
echo "🔐 Настраиваем права доступа..."
chown -R www-data:www-data /var/www/telegram_story_bot
chmod +x /var/www/telegram_story_bot/telegram_story_bot.py

# Копируем systemd сервис
echo "⚙️ Настраиваем systemd сервис..."
cp telegram-story-bot.service /etc/systemd/system/
systemctl daemon-reload

# Включаем и запускаем сервис
echo "🚀 Запускаем сервис..."
systemctl enable telegram-story-bot
systemctl start telegram-story-bot

# Проверяем статус
echo "📊 Проверяем статус сервиса..."
systemctl status telegram-story-bot --no-pager

# Настраиваем Apache (опционально)
echo "🌐 Настраиваем Apache..."
cat > /etc/apache2/sites-available/telegram-bot.conf << EOF
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /var/www/telegram_story_bot
    
    <Directory /var/www/telegram_story_bot>
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog \${APACHE_LOG_DIR}/telegram-bot-error.log
    CustomLog \${APACHE_LOG_DIR}/telegram-bot-access.log combined
</VirtualHost>
EOF

# Включаем сайт
a2ensite telegram-bot.conf
systemctl reload apache2

echo "✅ Деплой завершен успешно!"
echo ""
echo "📋 Полезные команды:"
echo "  Статус бота: systemctl status telegram-story-bot"
echo "  Остановить: systemctl stop telegram-story-bot"
echo "  Запустить: systemctl start telegram-story-bot"
echo "  Перезапустить: systemctl restart telegram-story-bot"
echo "  Логи: journalctl -u telegram-story-bot -f"
echo ""
echo "📁 Файлы проекта: /var/www/telegram_story_bot"
echo "📝 Логи бота: /var/www/telegram_story_bot/bot.log"
echo ""
echo "⚠️  Не забудьте настроить config.ini с вашими данными!"
