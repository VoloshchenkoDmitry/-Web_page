import os
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category


class ProductForm(forms.ModelForm):
    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Стилизация полей формы
        for field_name, field in self.fields.items():
            if field_name == 'description':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Введите описание продукта'
                })
            elif field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['accept'] = 'image/jpeg,image/png'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название продукта'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = '0.00'

        # Ограничиваем выбор статуса для обычных пользователей
        if self.user and not (self.user.has_perm('catalog.can_unpublish_product') or
                              self.user.groups.filter(name='Модератор продуктов').exists()):
            self.fields['status'].choices = [
                ('draft', 'Черновик'),
                ('published', 'Опубликовано'),
            ]

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data.get('name', '').lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(
                    f'Название продукта содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания продукта"""
        description = self.cleaned_data.get('description', '').lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(
                    f'Описание продукта содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """Валидация цены продукта"""
        price = self.cleaned_data.get('price')

        if price is None:
            return price

        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')

        if price == 0:
            raise ValidationError('Цена не может быть нулевой')

        return price

    def clean_image(self):
        """Валидация загружаемого изображения"""
        image = self.cleaned_data.get('image')

        if image:
            # Проверка размера файла (5 МБ)
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('Размер файла не должен превышать 5 МБ')

            # Проверка формата файла
            valid_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError('Поддерживаются только файлы JPEG и PNG')

            # Проверка MIME типа
            valid_mime_types = ['image/jpeg', 'image/png']
            if hasattr(image, 'content_type') and image.content_type not in valid_mime_types:
                raise ValidationError('Недопустимый тип файла')

        return image