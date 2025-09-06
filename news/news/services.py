import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from django.contrib.auth.models import User
from .models import PendingNews


class NewsScrapingService:
    """Сервис для загрузки новостей по теме нейросети"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_neural_network_news(self, count=5):
        """Поиск новостей по теме нейросети (демо-генерация на нужное количество)"""
        # Базовые примеры для шаблона
        base_samples = [
            {
                'title': 'Новый прорыв в области нейронных сетей: GPT-5 показывает удивительные результаты',
                'description': 'Исследователи OpenAI представили новую модель GPT-5, которая демонстрирует беспрецедентные возможности в понимании контекста и генерации текста.',
                'content': (
                    'Компания OpenAI объявила о создании новой языковой модели GPT-5, которая превосходит все предыдущие версии '\
                    'по качеству генерации текста и пониманию контекста.'
                ),
                'source_url': 'https://example.com/news/gpt5-breakthrough',
                'image_url': 'https://placehold.co/600x300/0066cc/ffffff?text=GPT-5+News'
            },
            {
                'title': 'Российские ученые создали нейросеть для диагностики рака на ранних стадиях',
                'description': 'Команда исследователей из МГУ разработала ИИ-систему, способную обнаруживать онкологические заболевания с точностью 97%.',
                'content': (
                    'Российские ученые из МГУ имени М.В. Ломоносова представили революционную нейронную сеть для '\
                    'ранней диагностики онкологических заболеваний.'
                ),
                'source_url': 'https://example.com/news/russian-cancer-ai',
                'image_url': 'https://placehold.co/600x300/cc6600/ffffff?text=Medical+AI'
            },
            {
                'title': 'Нейросети научились создавать 3D-модели из текстовых описаний',
                'description': 'Новая технология от Google позволяет генерировать детализированные трехмерные объекты на основе текстовых промптов.',
                'content': (
                    'Google представила инновационную технологию DreamFusion 3D, которая создает трехмерные модели '\
                    'объектов на основе текстовых описаний.'
                ),
                'source_url': 'https://example.com/news/3d-text-generation',
                'image_url': 'https://placehold.co/600x300/009900/ffffff?text=3D+Generation'
            },
        ]

        generated = []
        for i in range(count):
            sample = base_samples[i % len(base_samples)].copy()
            # Делаем заголовки уникальными, чтобы в админке было видно N разных элементов
            sample['title'] = f"{sample['title']} #{i + 1}"
            # Небольшая вариация source_url для уникальности
            sample['source_url'] = f"{sample['source_url']}?n={i+1}"
            generated.append(sample)

        return generated
    
    def save_pending_news(self, news_data, user):
        """Сохранение новости для модерации"""
        try:
            pending_news = PendingNews.objects.create(
                title=news_data['title'],
                short_description=news_data['description'],
                text=news_data['content'],
                source_url=news_data['source_url'],
                image_url=news_data.get('image_url', ''),
                created_by=user
            )
            return pending_news
        except Exception as e:
            print(f"Ошибка при сохранении новости: {e}")
            return None
    
    def load_news_batch(self, user, count=5):
        """Загрузка партии новостей для модерации"""
        news_list = self.search_neural_network_news(count)
        saved_news = []
        
        for news_data in news_list:
            saved_news_item = self.save_pending_news(news_data, user)
            if saved_news_item:
                saved_news.append(saved_news_item)
        
        return saved_news
