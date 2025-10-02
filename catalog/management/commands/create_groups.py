from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы модераторов и контент-менеджеров с соответствующими правами'

    def handle(self, *args, **options):
        # Получаем ContentType для моделей
        product_content_type = ContentType.objects.get_for_model(Product)

        # Получаем разрешения для продуктов
        product_permissions = Permission.objects.filter(content_type=product_content_type)

        # Создаем группу "Модератор продуктов"
        product_moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            # Добавляем права для модератора продуктов
            product_moderator_permissions = [
                'can_unpublish_product',
                'delete_product',  # Удаление любого продукта
                'change_product',  # Изменение любого продукта
                'view_product',  # Просмотр любого продукта
            ]

            for perm_codename in product_moderator_permissions:
                try:
                    permission = Permission.objects.get(
                        content_type=product_content_type,
                        codename=perm_codename
                    )
                    product_moderator_group.permissions.add(permission)
                    self.stdout.write(
                        self.style.SUCCESS(f'Добавлено разрешение: {perm_codename}')
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Разрешение {perm_codename} не найдено')
                    )

            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" создана успешно')
            )
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Создаем группу "Контент-менеджер"
        try:
            from blog.models import BlogPost
            blog_content_type = ContentType.objects.get_for_model(BlogPost)

            content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
            if created:
                # Добавляем права для контент-менеджера
                content_manager_permissions = [
                    'add_blogpost',
                    'change_blogpost',
                    'delete_blogpost',
                    'view_blogpost',
                ]

                for perm_codename in content_manager_permissions:
                    try:
                        permission = Permission.objects.get(
                            content_type=blog_content_type,
                            codename=perm_codename
                        )
                        content_manager_group.permissions.add(permission)
                        self.stdout.write(
                            self.style.SUCCESS(f'Добавлено разрешение: {perm_codename}')
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Разрешение {perm_codename} не найдено')
                        )

                self.stdout.write(
                    self.style.SUCCESS('Группа "Контент-менеджер" создана успешно')
                )
            else:
                self.stdout.write('Группа "Контент-менеджер" уже существует')

        except ImportError:
            self.stdout.write(
                self.style.WARNING('Приложение blog не установлено, группа "Контент-менеджер" не создана')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании группы "Контент-менеджер": {e}')
            )

        self.stdout.write(
            self.style.SUCCESS('Все группы созданы и настроены успешно')
        )