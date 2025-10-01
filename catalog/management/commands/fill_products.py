from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from users.models import User
import random


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми категориями и продуктами'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем тестового пользователя если нет
        try:
            user = User.objects.get(email='test@example.com')
        except User.DoesNotExist:
            user = User.objects.create_user(
                email='test@example.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )

        # Создаем категории
        categories_data = [
            {
                'name': 'Рассылки',
                'description': 'Сервисы для email рассылок и уведомлений'
            },
            {
                'name': 'Телеграм боты',
                'description': 'Боты для Telegram с различным функционалом'
            },
            {
                'name': 'Веб-приложения',
                'description': 'Готовые веб-приложения и SaaS решения'
            },
            {
                'name': 'Полезные утилиты',
                'description': 'Вспомогательные программы и инструменты'
            },
            {
                'name': 'Микросервисы',
                'description': 'Микросервисная архитектура и API'
            },
            {
                'name': 'Мобильные приложения',
                'description': 'Приложения для iOS и Android'
            },
        ]

        categories = []
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories.append(category)
            self.stdout.write(f'Создана категория: {category.name}')

        # Создаем продукты
        products_data = [
            {
                'name': 'Email рассылка PRO',
                'description': 'Профессиональный сервис для массовых email рассылок с аналитикой и A/B тестированием. Поддержка сегментации аудитории и автоматических цепочек писем.',
                'price': 199.99,
                'category': 'Рассылки',
                'status': 'published'
            },
            {
                'name': 'Telegram бот для магазина',
                'description': 'Умный бот для интернет-магазина с интеграцией платежных систем, управлением заказами и автоматическим оповещением клиентов.',
                'price': 299.99,
                'category': 'Телеграм боты',
                'status': 'published'
            },
            {
                'name': 'Интернет-магазин под ключ',
                'description': 'Готовое решение для интернет-магазина с адаптивным дизайном, корзиной покупок и интеграцией с популярными платежными системами.',
                'price': 499.99,
                'category': 'Веб-приложения',
                'status': 'published'
            },
            {
                'name': 'API Gateway Enterprise',
                'description': 'Мощный API шлюз для управления микросервисной архитектурой с мониторингом, кешированием и ограничением запросов.',
                'price': 399.99,
                'category': 'Микросервисы',
                'status': 'published'
            },
            {
                'name': 'Утилита для бэкапов',
                'description': 'Автоматизированная утилита для резервного копирования данных с поддержкой облачных хранилищ и шифрованием.',
                'price': 149.99,
                'category': 'Полезные утилиты',
                'status': 'published'
            },
            {
                'name': 'CRM система для малого бизнеса',
                'description': 'Комплексная CRM система с управлением клиентами, задачами, сделками и аналитикой продаж.',
                'price': 599.99,
                'category': 'Веб-приложения',
                'status': 'published'
            },
            {
                'name': 'Чат-бот поддержки',
                'description': 'AI-чатбот для автоматизации службы поддержки с обучением на ваших данных и интеграцией с популярными мессенджерами.',
                'price': 249.99,
                'category': 'Телеграм боты',
                'status': 'published'
            },
            {
                'name': 'Авто-рассыльщик писем',
                'description': 'Автоматизированная система для триггерных рассылок с персонализацией и отслеживанием эффективности.',
                'price': 179.99,
                'category': 'Рассылки',
                'status': 'published'
            },
            {
                'name': 'Мобильное приложение для доставки',
                'description': 'Кроссплатформенное мобильное приложение для службы доставки с трекингом заказов и push-уведомлениями.',
                'price': 699.99,
                'category': 'Мобильные приложения',
                'status': 'published'
            },
            {
                'name': 'Микросервис аутентификации',
                'description': 'Готовый микросервис для управления пользователями с поддержкой OAuth2, JWT и двухфакторной аутентификацией.',
                'price': 349.99,
                'category': 'Микросервисы',
                'status': 'published'
            },
            {
                'name': 'Утилита для мониторинга серверов',
                'description': 'Мощная утилита для мониторинга состояния серверов с алертами и детальной статистикой производительности.',
                'price': 199.99,
                'category': 'Полезные утилиты',
                'status': 'published'
            },
            {
                'name': 'Платформа для онлайн-курсов',
                'description': 'Полнофункциональная платформа для создания и продажи онлайн-курсов с видеоплеером, тестами и системой прогресса.',
                'price': 799.99,
                'category': 'Веб-приложения',
                'status': 'published'
            },
        ]

        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            product = Product.objects.create(
                name=prod_data['name'],
                description=prod_data['description'],
                category=category,
                price=prod_data['price'],
                status=prod_data['status'],
                owner=user
            )
            self.stdout.write(f'Создан продукт: {product.name} - {product.price} ₽')

        # Создаем несколько черновиков
        draft_products = [
            {
                'name': 'Новый мессенджер бот',
                'description': 'Инновационный бот для мессенджеров с AI-функционалом (в разработке).',
                'price': 399.99,
                'category': 'Телеграм боты',
                'status': 'draft'
            },
            {
                'name': 'Облачная CRM',
                'description': 'Облачная CRM система с расширенной аналитикой (планируется к выпуску).',
                'price': 899.99,
                'category': 'Веб-приложения',
                'status': 'draft'
            },
        ]

        for draft_data in draft_products:
            category = Category.objects.get(name=draft_data['category'])
            product = Product.objects.create(
                name=draft_data['name'],
                description=draft_data['description'],
                category=category,
                price=draft_data['price'],
                status=draft_data['status'],
                owner=user
            )
            self.stdout.write(f'Создан черновик: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {len(categories)} категорий и {len(products_data) + len(draft_products)} продуктов'
            )
        )