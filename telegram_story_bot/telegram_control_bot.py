#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import configparser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram_story_bot import TelegramStoryBot
import threading
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('control_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TelegramControlBot:
    def __init__(self, config_path: str = 'config.ini'):
        """Инициализация бота управления"""
        self.config = self.load_config(config_path)
        self.bot_token = self.config['DEFAULT']['bot_token']
        self.admin_ids = [int(x.strip()) for x in self.config['DEFAULT']['admins'].split(',')]
        
        # Экземпляр основного бота
        self.story_bot = None
        self.story_bot_thread = None
        
        # Инициализация Telegram бота
        self.application = Application.builder().token(self.bot_token).build()
        self.setup_handlers()
        
        logger.info("Бот управления инициализирован")
    
    def load_config(self, config_path: str) -> configparser.ConfigParser:
        """Загрузка конфигурации"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден")
        
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        return config
    
    def is_admin(self, user_id: int) -> bool:
        """Проверка, является ли пользователь администратором"""
        return user_id in self.admin_ids
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("start_bot", self.start_story_bot))
        self.application.add_handler(CommandHandler("stop_bot", self.stop_story_bot))
        self.application.add_handler(CommandHandler("test_story", self.test_story))
        self.application.add_handler(CommandHandler("feed_info", self.feed_info))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для управления ботом.")
            return
        
        keyboard = [
            [
                InlineKeyboardButton("📊 Статус", callback_data="status"),
                InlineKeyboardButton("▶️ Запустить", callback_data="start_bot")
            ],
            [
                InlineKeyboardButton("⏹️ Остановить", callback_data="stop_bot"),
                InlineKeyboardButton("🧪 Тест сторис", callback_data="test_story")
            ],
            [
                InlineKeyboardButton("📋 Инфо о фиде", callback_data="feed_info"),
                InlineKeyboardButton("❓ Помощь", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🤖 **Telegram Story Bot - Панель управления**\n\n"
            "Выберите действие:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = """
🤖 **Telegram Story Bot - Справка**

**Команды:**
• `/start` - Главное меню
• `/status` - Статус бота
• `/start_bot` - Запустить бота
• `/stop_bot` - Остановить бота
• `/test_story` - Создать тестовую сторис
• `/feed_info` - Информация о фиде
• `/help` - Эта справка

**Функции:**
• Автоматическое размещение сторис по расписанию
• Получение контента из XML фида
• Настраиваемые шаблоны текста
• Управление через Telegram

**Настройка:**
Отредактируйте файл `config.ini` для настройки:
• Времени размещения сторис
• URL фида
• Шаблонов текста
• ID администраторов
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /status"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для управления ботом.")
            return
        
        await self.send_status(update, context)
    
    async def send_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отправка статуса бота"""
        if self.story_bot is None:
            status_text = "📊 **Статус бота:**\n\n❌ Бот не инициализирован"
        else:
            try:
                status = self.story_bot.get_status()
                status_text = f"""
📊 **Статус бота:**

🔄 **Состояние:** {'🟢 Запущен' if status['is_running'] else '🔴 Остановлен'}

⏰ **Время размещения:** {', '.join(status['story_times'])}
📅 **Дни недели:** {status['story_days']}
📦 **Товаров в кэше:** {status['feed_items_count']}
🔄 **Последнее обновление:** {status['last_feed_update'] or 'Нет данных'}

🌐 **URL фида:** `{status['feed_url']}`
👥 **Администраторы:** {', '.join(map(str, status['admin_ids']))}
📱 **Аккаунты:** {', '.join(map(str, status['account_ids']))}
                """
            except Exception as e:
                status_text = f"❌ Ошибка при получении статуса: {str(e)}"
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def start_story_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start_bot"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для управления ботом.")
            return
        
        if self.story_bot is None:
            try:
                self.story_bot = TelegramStoryBot()
                await update.message.reply_text("✅ Бот инициализирован")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка инициализации: {str(e)}")
                return
        
        if self.story_bot.is_running:
            await update.message.reply_text("⚠️ Бот уже запущен")
            return
        
        try:
            # Запускаем бота в отдельном потоке
            self.story_bot_thread = threading.Thread(target=self.story_bot.start_bot)
            self.story_bot_thread.daemon = True
            self.story_bot_thread.start()
            
            await update.message.reply_text("✅ Бот запущен успешно!")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка запуска: {str(e)}")
    
    async def stop_story_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /stop_bot"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для управления ботом.")
            return
        
        if self.story_bot is None:
            await update.message.reply_text("⚠️ Бот не инициализирован")
            return
        
        if not self.story_bot.is_running:
            await update.message.reply_text("⚠️ Бот уже остановлен")
            return
        
        try:
            self.story_bot.stop_bot()
            await update.message.reply_text("✅ Бот остановлен успешно!")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка остановки: {str(e)}")
    
    async def test_story(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /test_story"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для управления ботом.")
            return
        
        if self.story_bot is None:
            try:
                self.story_bot = TelegramStoryBot()
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка инициализации: {str(e)}")
                return
        
        try:
            await update.message.reply_text("🔄 Создаю тестовую сторис...")
            
            story_data = self.story_bot.create_story()
            if story_data:
                test_text = f"""
🧪 **Тестовая сторис создана:**

📝 **Заголовок:** {story_data['title']}
📄 **Текст:** {story_data['text']}
🖼️ **Изображение:** [Ссылка]({story_data['image_url']})

✅ Сторис готова к размещению!
                """
                await update.message.reply_text(test_text, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Не удалось создать тестовую сторис")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при создании сторис: {str(e)}")
    
    async def feed_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /feed_info"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав для управления ботом.")
            return
        
        if self.story_bot is None:
            try:
                self.story_bot = TelegramStoryBot()
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка инициализации: {str(e)}")
                return
        
        try:
            await update.message.reply_text("🔄 Получаю информацию о фиде...")
            
            feed_data = self.story_bot.get_feed_data()
            if feed_data:
                feed_text = f"""
📋 **Информация о фиде:**

📦 **Всего товаров:** {len(feed_data)}

📝 **Примеры товаров:**
                """
                
                # Показываем первые 3 товара как пример
                for i, item in enumerate(feed_data[:3], 1):
                    title = self.story_bot.format_text(self.story_bot.title_template, item)
                    feed_text += f"\n{i}. {title}"
                
                if len(feed_data) > 3:
                    feed_text += f"\n\n... и еще {len(feed_data) - 3} товаров"
                
                await update.message.reply_text(feed_text, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Не удалось получить данные фида")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при получении информации о фиде: {str(e)}")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if not self.is_admin(user_id):
            await query.edit_message_text("❌ У вас нет прав для управления ботом.")
            return
        
        if query.data == "status":
            await self.send_status(update, context)
        elif query.data == "start_bot":
            await self.start_story_bot(update, context)
        elif query.data == "stop_bot":
            await self.stop_story_bot(update, context)
        elif query.data == "test_story":
            await self.test_story(update, context)
        elif query.data == "feed_info":
            await self.feed_info(update, context)
        elif query.data == "help":
            await self.help_command(update, context)
    
    def run(self):
        """Запуск бота"""
        logger.info("Запуск бота управления...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Главная функция"""
    try:
        control_bot = TelegramControlBot()
        control_bot.run()
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
