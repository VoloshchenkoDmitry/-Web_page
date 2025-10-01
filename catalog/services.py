from django.core.cache import cache
from django.db.models import Q
from .models import Product, Category


def get_products_by_category(category_slug, include_drafts=False, user=None):
    """
    Возвращает список продуктов в указанной категории с кешированием
    """
    cache_key = f'products_category_{category_slug}_{include_drafts}'
    if user and user.is_authenticated:
        cache_key += f'_user_{user.id}'

    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    try:
        category = Category.objects.get(name=category_slug)
    except Category.DoesNotExist:
        return []

    queryset = Product.objects.filter(category=category)

    # Фильтруем по статусу
    if not include_drafts:
        queryset = queryset.filter(status='published')
    elif user and user.is_authenticated:
        # Для авторизованных пользователей показываем их черновики + опубликованные
        queryset = queryset.filter(
            Q(status='published') |
            Q(status='draft', owner=user)
        )

    products = list(queryset.order_by('-created_at'))

    # Кешируем на 10 минут
    cache.set(cache_key, products, 60 * 10)

    return products


def get_cached_categories():
    """
    Возвращает кешированный список категорий
    """
    cache_key = 'all_categories'
    cached_categories = cache.get(cache_key)

    if cached_categories is not None:
        return cached_categories

    categories = list(Category.objects.all().order_by('name'))
    cache.set(cache_key, categories, 60 * 30)  # Кешируем на 30 минут

    return categories


def get_cached_products():
    """
    Возвращает кешированный список всех опубликованных продуктов
    """
    cache_key = 'all_published_products'
    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    products = list(Product.objects.filter(status='published').order_by('-created_at'))
    cache.set(cache_key, products, 60 * 5)  # Кешируем на 5 минут

    return products


def get_cached_categories_with_counts():
    """
    Возвращает кешированный список категорий с количеством продуктов
    """
    cache_key = 'categories_with_counts'
    cached_categories = cache.get(cache_key)

    if cached_categories is not None:
        return cached_categories

    categories = Category.objects.all().order_by('name')
    categories_with_counts = []

    for category in categories:
        product_count = Product.objects.filter(
            category=category,
            status='published'
        ).count()

        categories_with_counts.append({
            'category': category,
            'product_count': product_count
        })

    cache.set(cache_key, categories_with_counts, 60 * 30)  # 30 минут

    return categories_with_counts


def get_cached_product_list(include_drafts=False, user=None, category_slug=None):
    """
    Низкоуровневое кеширование списка продуктов с фильтрацией
    """
    # Создаем ключ кеша на основе параметров
    cache_key_parts = ['product_list']

    if include_drafts and user and user.is_authenticated:
        cache_key_parts.append(f'drafts_user_{user.id}')
    elif include_drafts:
        cache_key_parts.append('all_drafts')
    else:
        cache_key_parts.append('published_only')

    if category_slug:
        cache_key_parts.append(f'category_{category_slug}')

    cache_key = '_'.join(cache_key_parts)

    # Пытаемся получить данные из кеша
    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    # Если в кеше нет, выполняем запрос к БД
    queryset = Product.objects.select_related('category', 'owner')

    # Фильтрация по категории
    if category_slug:
        queryset = queryset.filter(category__name=category_slug)

    # Фильтрация по статусу
    if not include_drafts:
        queryset = queryset.filter(status='published')
    elif user and user.is_authenticated:
        # Для авторизованных пользователей показываем их черновики + опубликованные
        queryset = queryset.filter(
            Q(status='published') |
            Q(status='draft', owner=user)
        )

    products = list(queryset.order_by('-created_at'))

    # Сохраняем в кеш на 5 минут
    cache.set(cache_key, products, 60 * 5)

    return products


def get_cached_featured_products(limit=6):
    """
    Возвращает кешированный список избранных продуктов
    """
    cache_key = f'featured_products_{limit}'
    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    products = list(Product.objects.filter(
        status='published'
    ).order_by('-created_at')[:limit])

    cache.set(cache_key, products, 60 * 10)  # 10 минут

    return products


def invalidate_product_cache(product_id=None, category_slug=None):
    """
    Инвалидирует кеш продуктов
    """
    if product_id:
        # Инвалидируем кеш конкретного продукта
        cache.delete(f'product_{product_id}')

    if category_slug:
        # Инвалидируем кеш категории
        cache.delete(f'products_category_{category_slug}_False')
        cache.delete(f'products_category_{category_slug}_True')

    # Инвалидируем общий кеш
    cache.delete('all_published_products')
    cache.delete('all_categories')
    cache.delete('categories_with_counts')

    # Инвалидируем все product_list кеши
    for key in cache.keys('product_list*'):
        cache.delete(key)