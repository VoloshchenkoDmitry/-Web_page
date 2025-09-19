# Web_page

Проект для управления каталогом плагинов и примеров кода.

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте окружение: `source venv/bin/activate` (Linux/Mac) или `venv\Scripts\activate` (Windows)
4. Установите зависимости: `pip install -r requirements.txt`
5. Примените миграции: `python manage.py migrate`
6. Запустите сервер: `python manage.py runserver`

## Структура проекта

- `catalog/` - основное приложение с каталогом товаров
- `config/` - настройки проекта

