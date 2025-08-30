#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import configparser
import requests
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET
import re

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TelegramStoryBot:
    def __init__(self, config_path: str = 'config.ini'):
        """Инициализация бота"""
        self.config = self.load_config(config_path)
        self.bot_token = self.config['DEFAULT']['bot_token']
        self.admin_ids = [int(x.strip()) for x in self.config['DEFAULT']['admins'].split(',')]
        self.account_ids = [int(x.strip()) for x in self.config['DEFAULT']['acccount'].split(',')]
        
        # Настройки контента
        self.feed_url = self.config['CONTENT']['URL']
        self.story_times = [x.strip() for x in self.config['CONTENT']['storys_time'].split(',')]
        self.story_days = self.config['CONTENT']['storys_days']
        self.title_template = self.config['CONTENT']['title']
        self.text_template = self.config['CONTENT']['text']
        
        # Состояние бота
        self.is_running = False
        self.scheduler = None
        
        # Кэш для хранения данных фида
        self.feed_cache = []
        self.last_feed_update = None
        
        logger.info("Бот инициализирован")
    
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
    
    def get_feed_data(self) -> List[Dict]:
        """Получение данных из фида (учет категорий, параметров и нескольких картинок)"""
        try:
            response = requests.get(self.feed_url, timeout=30)
            response.raise_for_status()

            root = ET.fromstring(response.content)

            # Построение словаря категорий id -> название
            categories_map: Dict[str, str] = {}
            categories_root = root.find('.//categories')
            if categories_root is not None:
                for cat in categories_root.findall('category'):
                    cat_id = cat.attrib.get('id')
                    if cat_id:
                        categories_map[cat_id] = (cat.text or '').strip()

            offers: List[Dict] = []
            for offer in root.findall('.//offer'):
                offer_data: Dict[str, object] = {}

                # Атрибуты оффера
                for key, value in offer.attrib.items():
                    offer_data[key] = value

                pictures: List[str] = []

                # Дочерние элементы
                for child in offer:
                    tag = child.tag
                    text = (child.text or '').strip()

                    if tag == 'param':
                        # Поддержка <param name="..."></param> (например "модель", "год выпуска")
                        param_name = child.attrib.get('name')
                        if param_name:
                            offer_data[param_name] = text
                        continue

                    if tag == 'picture':
                        if text:
                            pictures.append(text)
                        # Сохраняем первый picture также под ключом 'picture' для совместимости
                        if 'picture' not in offer_data and text:
                            offer_data['picture'] = text
                        continue

                    # Обычные теги (берем последнее значение)
                    offer_data[tag] = text

                    # Сохраняем атрибуты дочерних тегов (например, <price currencyId="RUR">)
                    if child.attrib:
                        for attr_key, attr_val in child.attrib.items():
                            # Пишем атрибут как отдельное поле, например 'currencyId'
                            # Если такое поле уже есть, перезапишем последним значением
                            offer_data[attr_key] = attr_val

                # Категория из categoryId
                category_id = str(offer_data.get('categoryId', '')).strip()
                if category_id and categories_map:
                    offer_data['category'] = categories_map.get(category_id, '')

                # Список всех картинок
                if pictures:
                    offer_data['_pictures'] = pictures

                offers.append(offer_data)  # type: ignore[arg-type]

            logger.info(f"Получено {len(offers)} товаров из фида")
            return offers  # type: ignore[return-value]

        except Exception as e:
            logger.error(f"Ошибка при получении данных фида: {e}")
            return []
    
    def format_text(self, template: str, data: Dict) -> str:
        """Форматирование текста по шаблону"""
        try:
            # Заменяем поля в кавычках на значения из данных
            formatted_text = template
            
            # Находим все поля в кавычках
            pattern = r'"([^"]+)"'
            matches = re.findall(pattern, template)
            
            for field in matches:
                # Пробуем точное имя поля
                value = data.get(field, '')
                if value == '':
                    # Пробуем найти ключ без учета регистра
                    lower_field = field.lower()
                    for key, val in data.items():
                        if isinstance(key, str) and key.lower() == lower_field:
                            value = val
                            break
                formatted_text = formatted_text.replace(f'"{field}"', str(value))
            
            # Убираем лишние пробелы и запятые
            formatted_text = re.sub(r'\s+', ' ', formatted_text)
            formatted_text = re.sub(r',\s*,', ',', formatted_text)
            formatted_text = formatted_text.strip()
            
            return formatted_text
            
        except Exception as e:
            logger.error(f"Ошибка при форматировании текста: {e}")
            return "Ошибка форматирования"
    
    def get_random_item(self) -> Optional[Dict]:
        """Получение случайного товара из фида"""
        if not self.feed_cache:
            self.feed_cache = self.get_feed_data()
            self.last_feed_update = datetime.now()
        
        # Обновляем кэш каждый час
        if self.last_feed_update and datetime.now() - self.last_feed_update > timedelta(hours=1):
            self.feed_cache = self.get_feed_data()
            self.last_feed_update = datetime.now()
        
        if not self.feed_cache:
            return None
        
        import random
        return random.choice(self.feed_cache)
    
    def create_story(self) -> Optional[Dict]:
        """Создание сторис"""
        try:
            item = self.get_random_item()
            if not item:
                logger.warning("Не удалось получить товар для сторис")
                return None
            
            # Форматируем заголовок и текст
            title = self.format_text(self.title_template, item)
            text = self.format_text(self.text_template, item)
            
            # Получаем изображение (пробуем несколько возможных полей)
            image_url_candidates: List[str] = []
            if isinstance(item.get('_pictures'), list):
                image_url_candidates.extend([str(u) for u in item.get('_pictures', []) if u])
            for key in ['picture', 'image', 'image_url', 'photo', 'url']:
                val = item.get(key)
                if isinstance(val, str) and val:
                    image_url_candidates.append(val)

            image_url = next((u for u in image_url_candidates if u), '')
            if not image_url:
                logger.warning("URL изображения не найден")
                return None
            
            # Скачиваем изображение
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            story_data = {
                'title': title,
                'text': text,
                'image_data': response.content,
                'image_url': image_url
            }
            
            logger.info(f"Создана сторис: {title}")
            return story_data
            
        except Exception as e:
            logger.error(f"Ошибка при создании сторис: {e}")
            return None
    
    def post_story(self, story_data: Dict) -> bool:
        """Размещение сторис в Telegram"""
        try:
            # Здесь должна быть логика размещения сторис через Telegram API
            # Поскольку Telegram Bot API не поддерживает размещение сторис напрямую,
            # нужно использовать MTProto API или другие методы
            
            logger.info(f"Сторис размещена: {story_data['title']}")
            logger.info(f"Текст: {story_data['text']}")
            logger.info(f"Изображение: {story_data['image_url']}")
            
            # TODO: Реализовать размещение через MTProto API
            # Пока просто логируем
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при размещении сторис: {e}")
            return False
    
    def schedule_stories(self):
        """Планирование размещения сторис"""
        for time_str in self.story_times:
            schedule.every().day.at(time_str).do(self.post_scheduled_story)
            logger.info(f"Запланировано размещение сторис в {time_str}")
    
    def post_scheduled_story(self):
        """Размещение запланированной сторис"""
        if not self.is_running:
            return
        
        logger.info("Запуск запланированного размещения сторис")
        
        story_data = self.create_story()
        if story_data:
            success = self.post_story(story_data)
            if success:
                logger.info("Сторис успешно размещена")
            else:
                logger.error("Ошибка при размещении сторис")
        else:
            logger.warning("Не удалось создать сторис")
    
    def start_bot(self):
        """Запуск бота"""
        if self.is_running:
            logger.info("Бот уже запущен")
            return
        
        self.is_running = True
        self.schedule_stories()
        
        logger.info("Бот запущен")
        logger.info(f"Время размещения сторис: {', '.join(self.story_times)}")
        
        # Запускаем планировщик
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту
    
    def stop_bot(self):
        """Остановка бота"""
        self.is_running = False
        schedule.clear()
        logger.info("Бот остановлен")
    
    def get_status(self) -> Dict:
        """Получение статуса бота"""
        return {
            'is_running': self.is_running,
            'story_times': self.story_times,
            'story_days': self.story_days,
            'feed_url': self.feed_url,
            'admin_ids': self.admin_ids,
            'account_ids': self.account_ids,
            'last_feed_update': self.last_feed_update.isoformat() if self.last_feed_update else None,
            'feed_items_count': len(self.feed_cache)
        }

def main():
    """Главная функция"""
    try:
        bot = TelegramStoryBot()
        
        # Простой CLI интерфейс для управления
        print("Телеграм бот для размещения сторис")
        print("Команды: start, stop, status, exit")
        
        while True:
            command = input("Введите команду: ").strip().lower()
            
            if command == 'start':
                print("Запуск бота...")
                bot.start_bot()
            elif command == 'stop':
                print("Остановка бота...")
                bot.stop_bot()
            elif command == 'status':
                status = bot.get_status()
                print(f"Статус: {'Запущен' if status['is_running'] else 'Остановлен'}")
                print(f"Время размещения: {', '.join(status['story_times'])}")
                print(f"Товаров в кэше: {status['feed_items_count']}")
            elif command == 'exit':
                bot.stop_bot()
                print("Выход...")
                break
            else:
                print("Неизвестная команда")
    
    except KeyboardInterrupt:
        print("\nПолучен сигнал прерывания")
        if 'bot' in locals():
            bot.stop_bot()
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
