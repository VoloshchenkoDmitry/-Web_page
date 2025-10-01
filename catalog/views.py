from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.conf import settings
from .models import Product, Contact, Category
from .forms import ProductForm
from .utils import can_edit_product, can_delete_product, can_unpublish_product, is_product_moderator
from .services import get_products_by_category, get_cached_categories, get_cached_categories_with_counts, get_cached_product_list, get_cached_featured_products


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        # Используем низкоуровневое кеширование
        include_drafts = self.request.user.is_authenticated
        return get_cached_product_list(
            include_drafts=include_drafts,
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем кешированные категории и избранные продукты
        context['categories'] = get_cached_categories()
        context['featured_products'] = get_cached_featured_products(3)
        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = Contact.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Обработка формы
        messages.success(request, 'Сообщение успешно отправлено!')
        return redirect('catalog:contacts')


class CategoriesListView(ListView):
    model = Category
    template_name = 'catalog/categories_list.html'
    context_object_name = 'categories_with_counts'

    @method_decorator(cache_page(60 * 30))  # Кешируем на 30 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return get_cached_categories_with_counts()


class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    @method_decorator(cache_page(60 * 10))  # Кешируем на 10 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        include_drafts = self.request.user.is_authenticated

        return get_products_by_category(
            category_slug,
            include_drafts=include_drafts,
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')

        try:
            category = Category.objects.get(name=category_slug)
            context['category'] = category
            context['page_title'] = f'Продукты в категории: {category.name}'
        except Category.DoesNotExist:
            context['category'] = None
            context['page_title'] = 'Категория не найдена'

        context['categories'] = get_cached_categories()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    @method_decorator(cache_page(60 * 15))  # Кешируем на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Все могут видеть опубликованные продукты
        queryset = super().get_queryset().filter(status='published')

        # Авторизованные пользователи могут видеть свои черновики
        if self.request.user.is_authenticated:
            user_drafts = Product.objects.filter(
                owner=self.request.user,
                status='draft'
            )
            queryset = queryset.union(user_drafts)

        # Модераторы могут видеть все продукты
        if self.request.user.is_authenticated and is_product_moderator(self.request.user):
            queryset = super().get_queryset()

        return queryset


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Товар успешно добавлен!')

        # Инвалидируем кеш после создания продукта
        invalidate_product_cache()

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        product = self.get_object()
        return can_edit_product(self.request.user, product)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Товар успешно обновлен!')

        # Инвалидируем кеш после обновления продукта
        invalidate_product_cache(
            product_id=self.object.pk,
            category_slug=self.object.category.name if self.object.category else None
        )

        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для редактирования этого продукта.')
        return redirect('catalog:product_detail', pk=self.get_object().pk)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        return can_delete_product(self.request.user, product)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        category_slug = product.category.name if product.category else None

        # Инвалидируем кеш перед удалением
        invalidate_product_cache(
            product_id=product.pk,
            category_slug=category_slug
        )

        messages.success(self.request, 'Товар успешно удален!')
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этого продукта.')
        return redirect('catalog:product_detail', pk=self.get_object().pk)


class ProductPublishView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Product
    template_name = 'catalog/product_confirm_publish.html'

    def test_func(self):
        product = self.get_object()
        return (product.owner == self.request.user or
                can_unpublish_product(self.request.user))

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        action = request.POST.get('action')

        if action == 'publish':
            product.publish()
            messages.success(request, 'Продукт успешно опубликован!')
        elif action == 'unpublish':
            product.unpublish()
            messages.success(request, 'Публикация продукта отменена!')

        # Инвалидируем кеш после изменения статуса
        invalidate_product_cache(
            product_id=product.pk,
            category_slug=product.category.name if product.category else None
        )

        return redirect('catalog:product_detail', pk=product.pk)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения статуса публикации этого продукта.')
        return redirect('catalog:product_detail', pk=self.get_object().pk)