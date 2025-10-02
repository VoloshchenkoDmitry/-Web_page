from django.contrib.auth.models import Group

def is_product_moderator(user):
    """Проверяет, является ли пользователь модератором продуктов"""
    return user.groups.filter(name='Модератор продуктов').exists()

def is_content_manager(user):
    """Проверяет, является ли пользователь контент-менеджером"""
    return user.groups.filter(name='Контент-менеджер').exists()

def can_edit_product(user, product):
    """Проверяет, может ли пользователь редактировать продукт"""
    return user == product.owner or is_product_moderator(user)

def can_delete_product(user, product):
    """Проверяет, может ли пользователь удалить продукт"""
    return user == product.owner or is_product_moderator(user)

def can_unpublish_product(user):
    """Проверяет, может ли пользователь отменять публикацию продуктов"""
    return user.has_perm('catalog.can_unpublish_product') or is_product_moderator(user)