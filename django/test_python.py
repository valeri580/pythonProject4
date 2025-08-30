#!/usr/bin/env python3
"""
Тестовый файл для проверки работы Python в Cursor
"""

print("Python работает!")
print("Django проект находится в папке django/")

# Проверим импорт Django (если установлен)
try:
    import django
    print(f"Django версия: {django.get_version()}")
except ImportError:
    print("Django не установлен. Выполните: pip install Django")

# Информация о проекте
print("\n=== Структура Django проекта ===")
print("📁 django/")
print("  ├── manage.py")
print("  ├── mysite/ (настройки)")
print("  └── website/ (приложение)")
print("      └── templates/")
print("          ├── includes/ (меню и подвал)")
print("          └── website/ (4 страницы)")
