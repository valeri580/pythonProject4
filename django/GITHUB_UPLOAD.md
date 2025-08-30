# 🚀 Загрузка Django проекта на GitHub

## 📍 Ваш профиль GitHub
**https://github.com/valeri580**

## 🎯 Автоматическая настройка Git

### Способ 1: Через bat файл (рекомендуется)
1. Дважды кликните на `git_setup.bat`
2. Дождитесь завершения настройки
3. Следуйте инструкциям в консоли

### Способ 2: Ручная настройка
```bash
# 1. Добавить файлы
git add .

# 2. Создать коммит
git commit -m "Initial commit: Django website with Bootstrap and includes"

# 3. Настроить пользователя (если нужно)
git config user.name "valeri580"
git config user.email "valeri580@users.noreply.github.com"

# 4. Создать основную ветку
git branch -M main
```

## 🌐 Создание репозитория на GitHub

### Шаг 1: Создайте новый репозиторий
1. Перейдите на https://github.com/new
2. **Repository name**: `django-bootstrap-website`
3. **Description**: `Django website with 4 pages, Bootstrap styling, and separate includes for navbar and footer`
4. Выберите **Public** или **Private**
5. **НЕ** ставьте галочки на README, .gitignore, license (они уже есть)
6. Нажмите **Create repository**

### Шаг 2: Подключите удаленный репозиторий
```bash
git remote add origin https://github.com/valeri580/django-bootstrap-website.git
git push -u origin main
```

## 📁 Что будет загружено на GitHub

```
django-bootstrap-website/
├── 📄 README.md              ← Документация проекта
├── 📄 ЗАПУСК.md              ← Инструкция по запуску
├── 📄 .gitignore             ← Исключения для Git
├── 🚀 run_server.bat         ← Запуск Django сервера
├── 🔧 git_setup.bat          ← Настройка Git
├── ⚙️ manage.py              ← Django управление
├── 📄 requirements.txt       ← Зависимости
├── mysite/                   ← Настройки Django
│   ├── settings.py          ← Конфигурация
│   └── urls.py              ← Главные URL
└── website/                 ← Приложение сайта
    ├── views.py             ← Представления (4 страницы)
    ├── urls.py              ← URL маршруты
    └── templates/           ← ⭐ Шаблоны
        ├── includes/        ← 🎯 Отдельные файлы
        │   ├── navbar.html  ← Меню (через include)
        │   └── footer.html  ← Подвал (через include)
        └── website/         ← 🎯 4 страницы
            ├── base.html    ← Базовый шаблон
            ├── home.html    ← Главная
            ├── about.html   ← О нас
            ├── services.html ← Услуги
            └── contact.html ← Контакты
```

## ✅ Особенности проекта для GitHub

- ✅ **Django проект** с Bootstrap стилизацией
- ✅ **4 страницы**: Главная, О нас, Услуги, Контакты  
- ✅ **Отдельные файлы** для меню и подвала
- ✅ **Подключение через {% include %}**
- ✅ **Адаптивный дизайн**
- ✅ **Готовые инструкции** для запуска
- ✅ **Правильный .gitignore** для Django

## 🏷️ Рекомендуемые теги для репозитория

При создании репозитория добавьте теги:
- `django`
- `bootstrap`
- `python`
- `web-development`
- `templates`
- `includes`
- `responsive-design`

## 📝 Описание для GitHub

```
Django website with 4 pages styled with Bootstrap. 
Demonstrates the use of separate files for navbar and footer 
connected to the main template via {% include %}.

Features:
- 4 responsive pages (Home, About, Services, Contact)
- Bootstrap 5.3.0 styling
- Separate navbar.html and footer.html files
- Template inheritance and includes
- Ready-to-run Django project
```

## 🎉 После загрузки

Ваш проект будет доступен по адресу:
**https://github.com/valeri580/django-bootstrap-website**

Другие пользователи смогут:
1. Клонировать проект: `git clone https://github.com/valeri580/django-bootstrap-website.git`
2. Установить зависимости: `pip install -r requirements.txt`
3. Запустить сайт: `python manage.py runserver`
