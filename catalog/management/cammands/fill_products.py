from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import random


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми продуктами'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        categories = [
            {'name': 'Рассылки', 'description': 'Сервисы для email рассылок'},
            {'name': 'Телеграм боты', 'description': 'Боты для Telegram'},
            {'name': 'Веб-приложения', 'description': 'Веб-приложения и сайты'},
            {'name': 'Полезные утилиты', 'description': 'Вспомогательные программы'},
            {'name': 'Микросервисы', 'description': 'Микросервисная архитектура'},
        ]

        created_categories = []
        for cat_data in categories:
            category = Category.objects.create(**cat_data)
            created_categories.append(category)

        # Создаем продукты
        products = [
            {'name': 'Email рассылка PRO', 'price': 199.99, 'category': 'Рассылки'},
            {'name': 'Telegram бот для магазина', 'price': 299.99, 'category': 'Телеграм боты'},
            {'name': 'Интернет-магазин', 'price': 499.99, 'category': 'Веб-приложения'},
            {'name': 'API Gateway', 'price': 399.99, 'category': 'Микросервисы'},
            {'name': 'Утилита для бэкапов', 'price': 149.99, 'category': 'Полезные утилиты'},
            {'name': 'CRM система', 'price': 599.99, 'category': 'Веб-приложения'},
            {'name': 'Чат-бот поддержки', 'price': 249.99, 'category': 'Телеграм боты'},
            {'name': 'Авто-рассыльщик', 'price': 179.99, 'category': 'Рассылки'},
        ]

        for prod_data in products:
            category = Category.objects.get(name=prod_data['category'])
            Product.objects.create(
                name=prod_data['name'],
                description=f'Описание для {prod_data["name"]}',
                category=category,
                price=prod_data['price']
            )

        self.stdout.write(
            self.style.SUCCESS('Успешно создано %s категорий и %s продуктов' % (
                len(created_categories), len(products)
            ))
        )