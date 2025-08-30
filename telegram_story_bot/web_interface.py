#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from telegram_story_bot import TelegramStoryBot
import threading
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Измените на свой секретный ключ

# Глобальная переменная для хранения экземпляра бота
bot_instance = None
bot_thread = None

def create_bot():
    """Создание экземпляра бота"""
    global bot_instance
    try:
        bot_instance = TelegramStoryBot()
        return True
    except Exception as e:
        logger.error(f"Ошибка при создании бота: {e}")
        return False

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Получение статуса бота"""
    global bot_instance
    
    if bot_instance is None:
        return jsonify({
            'status': 'not_initialized',
            'message': 'Бот не инициализирован'
        })
    
    try:
        status = bot_instance.get_status()
        return jsonify({
            'status': 'success',
            'data': status
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Запуск бота"""
    global bot_instance, bot_thread
    
    if bot_instance is None:
        if not create_bot():
            return jsonify({
                'status': 'error',
                'message': 'Не удалось создать бота'
            })
    
    if bot_instance.is_running:
        return jsonify({
            'status': 'warning',
            'message': 'Бот уже запущен'
        })
    
    try:
        # Запускаем бота в отдельном потоке
        bot_thread = threading.Thread(target=bot_instance.start_bot)
        bot_thread.daemon = True
        bot_thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Бот запущен'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Остановка бота"""
    global bot_instance
    
    if bot_instance is None:
        return jsonify({
            'status': 'warning',
            'message': 'Бот не инициализирован'
        })
    
    if not bot_instance.is_running:
        return jsonify({
            'status': 'warning',
            'message': 'Бот уже остановлен'
        })
    
    try:
        bot_instance.stop_bot()
        return jsonify({
            'status': 'success',
            'message': 'Бот остановлен'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/test_story', methods=['POST'])
def test_story():
    """Тестовое создание сторис"""
    global bot_instance
    
    if bot_instance is None:
        if not create_bot():
            return jsonify({
                'status': 'error',
                'message': 'Не удалось создать бота'
            })
    
    try:
        story_data = bot_instance.create_story()
        if story_data:
            return jsonify({
                'status': 'success',
                'message': 'Тестовая сторис создана',
                'data': {
                    'title': story_data['title'],
                    'text': story_data['text'],
                    'image_url': story_data['image_url']
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Не удалось создать тестовую сторис'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/api/feed_info')
def get_feed_info():
    """Получение информации о фиде"""
    global bot_instance
    
    if bot_instance is None:
        if not create_bot():
            return jsonify({
                'status': 'error',
                'message': 'Не удалось создать бота'
            })
    
    try:
        feed_data = bot_instance.get_feed_data()
        return jsonify({
            'status': 'success',
            'data': {
                'items_count': len(feed_data),
                'sample_items': feed_data[:3] if feed_data else []
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    # Создаем папку для шаблонов
    os.makedirs('templates', exist_ok=True)
    
    # Создаем HTML шаблон
    html_template = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Story Bot - Управление</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .status-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
        }
        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: #007bff;
            color: white;
        }
        .btn-primary:hover {
            background: #0056b3;
        }
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        .btn-danger:hover {
            background: #c82333;
        }
        .btn-success {
            background: #28a745;
            color: white;
        }
        .btn-success:hover {
            background: #218838;
        }
        .btn-warning {
            background: #ffc107;
            color: #212529;
        }
        .btn-warning:hover {
            background: #e0a800;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }
        .info-label {
            font-weight: bold;
            color: #495057;
            margin-bottom: 5px;
        }
        .info-value {
            color: #6c757d;
        }
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .alert-success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .alert-danger {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .alert-warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007bff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Telegram Story Bot</h1>
        
        <div id="alerts"></div>
        
        <div class="status-card">
            <h3>Статус бота</h3>
            <div id="status-info">Загрузка...</div>
        </div>
        
        <div class="button-group">
            <button class="btn btn-success" onclick="startBot()">▶️ Запустить</button>
            <button class="btn btn-danger" onclick="stopBot()">⏹️ Остановить</button>
            <button class="btn btn-warning" onclick="testStory()">🧪 Тест сторис</button>
            <button class="btn btn-primary" onclick="refreshStatus()">🔄 Обновить</button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Выполняется операция...</p>
        </div>
        
        <div class="info-grid" id="info-grid" style="display: none;">
            <div class="info-item">
                <div class="info-label">Время размещения:</div>
                <div class="info-value" id="story-times">-</div>
            </div>
            <div class="info-item">
                <div class="info-label">Товаров в кэше:</div>
                <div class="info-value" id="feed-count">-</div>
            </div>
            <div class="info-item">
                <div class="info-label">Последнее обновление:</div>
                <div class="info-value" id="last-update">-</div>
            </div>
            <div class="info-item">
                <div class="info-label">URL фида:</div>
                <div class="info-value" id="feed-url">-</div>
            </div>
        </div>
    </div>

    <script>
        function showAlert(message, type = 'success') {
            const alertsDiv = document.getElementById('alerts');
            const alert = document.createElement('div');
            alert.className = `alert alert-${type}`;
            alert.textContent = message;
            alertsDiv.appendChild(alert);
            
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
        
        async function refreshStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                const statusInfo = document.getElementById('status-info');
                const infoGrid = document.getElementById('info-grid');
                
                if (data.status === 'success') {
                    const status = data.data;
                    statusInfo.innerHTML = `
                        <strong>Статус:</strong> ${status.is_running ? '🟢 Запущен' : '🔴 Остановлен'}
                    `;
                    
                    document.getElementById('story-times').textContent = status.story_times.join(', ');
                    document.getElementById('feed-count').textContent = status.feed_items_count;
                    document.getElementById('last-update').textContent = status.last_feed_update || 'Нет данных';
                    document.getElementById('feed-url').textContent = status.feed_url;
                    
                    infoGrid.style.display = 'grid';
                } else {
                    statusInfo.innerHTML = `<strong>Статус:</strong> ${data.message}`;
                    infoGrid.style.display = 'none';
                }
            } catch (error) {
                showAlert('Ошибка при получении статуса: ' + error.message, 'danger');
            }
        }
        
        async function startBot() {
            showLoading();
            try {
                const response = await fetch('/api/start', { method: 'POST' });
                const data = await response.json();
                showAlert(data.message, data.status);
                if (data.status === 'success') {
                    setTimeout(refreshStatus, 1000);
                }
            } catch (error) {
                showAlert('Ошибка при запуске бота: ' + error.message, 'danger');
            } finally {
                hideLoading();
            }
        }
        
        async function stopBot() {
            showLoading();
            try {
                const response = await fetch('/api/stop', { method: 'POST' });
                const data = await response.json();
                showAlert(data.message, data.status);
                if (data.status === 'success') {
                    setTimeout(refreshStatus, 1000);
                }
            } catch (error) {
                showAlert('Ошибка при остановке бота: ' + error.message, 'danger');
            } finally {
                hideLoading();
            }
        }
        
        async function testStory() {
            showLoading();
            try {
                const response = await fetch('/api/test_story', { method: 'POST' });
                const data = await response.json();
                showAlert(data.message, data.status);
            } catch (error) {
                showAlert('Ошибка при создании тестовой сторис: ' + error.message, 'danger');
            } finally {
                hideLoading();
            }
        }
        
        // Загружаем статус при загрузке страницы
        document.addEventListener('DOMContentLoaded', refreshStatus);
        
        // Обновляем статус каждые 30 секунд
        setInterval(refreshStatus, 30000);
    </script>
</body>
</html>
    '''
    
    # Сохраняем HTML шаблон
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print("🌐 Веб-интерфейс запущен на http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
