# Автоматизированная система для скачивания космических фотографий (SpaceX, NASA APOD, NASA EPIC) и публикация в Telegram-канал через бота.
### Проект состоит из:
1. Скрипты: `download_utils.py` и `file_utils.py` вспомогательные функции для работы с файлами: скачивание изображение по URL и схранение в указанную папку и извлечение расширения файла из URL.
2. Скрипты: `fetch_spacex_images.py`, `fetch_nasa_images.py` и `fetch_epic_images.py` автоматическая загрузка снимков, сохранение изображений и данных в указанную директорию.
- `fetch_spacex_images.py` - получает фотографии последнего запуска SpaceX (или указанного по ID).
- `fetch_nasa_images.py` - получает фотографии NASA через API по несколько картинок сразу, в одном запросе.
- `fetch_epic_images.py` - получает фотографии нашей планеты NASA EPIC.
3. `tg_bot.py` - базовый модуль для работы с Telegram API: содержит функции отправки текста, фото в группу Telegram.
4. `publication_tg_bot.py` - телеграм-бот для периодической публикации изображений в чат/канал с настраиваемым интервалом и дополнительными опциями.

## Функционал
- Автоматический сбор фотографий космоса
- Автопубликация в Telegram-канал


## Требования
- `Python3`
- Учетные записи:
    - [NASA API Key](https://api.nasa.gov/)
    - [Telegram Bot Token](https://way23.ru/регистрация-бота-в-telegram.html)

Чтобы запустить скрипт на `Python`, вам нужен интерпретатор `Python`. `Pip` понадобится, чтобы ставить библиотеки других разработчиков.
Установить `python` по [ссылка на официальный сайт](https://www.python.org/).

**Установить среду разработки**

[Статья о выборе среды](https://tproger.ru/articles/python-ide)

## Как установить
1. Клонируйте репозиторий

Репозиторий принадлежит не вам, поэтому стоит создать свою собственную копию репозитория. Это называется форком. [Как создать форк (вилку)](https://docs.github.com/ru/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости

**Основные зависимости:**
- `python = "3.12.4"`
- `python-dotenv = "*"` - для работы с переменными окружения
- `python-telegram-bot = "==13.0"` - 

Программа не будет работать без библиотеки `requests`, а она не входит в стандартную библиотеку `Python`. Поставьте её на свой компьютер с помощью [pip](https://dvmn.org/encyclopedia/pip/pip_basic_usage/).

```bash
pip install -r requirements.txt
```

4. Проверьте установку
```bash
python --version  # Должна быть версия Python 3*
pip list          # Должны отобразиться python-dotenv и requests
```

## Настройка

**Настройка переменных окружения**

Переменные окружения придётся загружать вручную при каждом запуске терминала. Автоматизируйте процесс с помощью модуля [python-dotenv](https://pypi.org/project/python-dotenv/0.9.1/).

**Переменные:**
- NASA_API - токен доступа для работы с NASA API
- TG_BOT_TOKEN - токен Telegram-бота
- TG_GROUP_CHAT_ID - ID чата/канала для отправки сообщений (Добавьте бота в канал/чат)

1. Создать файл `.env` в корне проекта:
- NASA_API=ваш_токен_здесь
- TG_BOT_TOKEN=ваш_токен_здесь
- TG_GROUP_CHAT_ID=ваш_ID_здесь

2. Добавьте `.env` в `.gitignore` чтобы не публиковать конфиденциальные данные.

## Запуск
После настройки окружения и установки зависимостей запустите скрипт.

Открыть терминал и ввести:
```bash
python fetch_spacex_images.py --help    # SpaceX photos
python fetch_nasa_images.py --help      # NASA APOD
python fetch_epic_images.py --help      # NASA EPIC
```

Автопубликация в Telegram:
```bash
python publication_tg_bot.py --help
```
![Снимок экрана 2025-06-10 133421](https://github.com/user-attachments/assets/ae06d403-aff3-47ab-b55d-0c2bb8d7cf23)


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
