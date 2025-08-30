Запуск сравнения генерации сторис (OpenAI, Yandex, GigaChat)

1) Установите зависимости:

```
py -m pip install --user -U python-dotenv requests
```

2) Подготовьте переменные окружения (создайте `.env` в корне проекта или рядом с файлами):

```
# OpenAI
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# Yandex
YANDEX_API_KEY=
YANDEX_FOLDER_ID=
YANDEX_MODEL=gpt://{folder_id}/yandexgpt-lite

# GigaChat
AUTHORIZATION_KEY= # base64(client_id:client_secret) или вместо этого CLIENT_ID/CLIENT_SECRET
CLIENT_ID=
CLIENT_SECRET=
SCOPE=GIGACHAT_API_PERS
# опционально: ACCESS_TOKEN=
```

3) Запуск:

```
py -m new.story_compare.run_compare
```

Результаты будут в `new/story_compare/output`: по одному файлу на провайдера и `report.txt` с кратким итогом.


