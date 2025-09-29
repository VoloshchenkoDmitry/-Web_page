from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import Product, Contact
from .forms import ProductForm


class HomeView(ListView):
    """Главная страница - доступна всем пользователям"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        # Вывод в консоль для дополнительного задания
        print("Последние 5 продуктов:")
        for product in queryset[:5]:
            print(f"- {product.name} ({product.price})")
        return queryset


class ContactsView(TemplateView):
    """Страница контактов - доступна всем пользователям"""
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = Contact.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        """Обработка формы обратной связи"""
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно добавить логику обработки формы
        # Например, сохранение в базу данных или отправка email

        messages.success(request, 'Сообщение успешно отправлено!')
        return redirect('catalog:contacts')


class ProductDetailView(DetailView):
    """Детальная страница продукта - доступна всем пользователям"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта - только для авторизованных пользователей"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Обработка успешного создания продукта"""
        messages.success(self.request, 'Товар успешно добавлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка ошибок валидации формы"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Добавляем дополнительный контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание нового продукта'
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта - только для авторизованных пользователей"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        """Перенаправление после успешного редактирования"""
        messages.success(self.request, 'Товар успешно обновлен!')
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        """Обработка ошибок валидации формы"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Добавляем дополнительный контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование продукта'
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта - только для авторизованных пользователей"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def delete(self, request, *args, **kwargs):
        """Обработка успешного удаления"""
        messages.success(self.request, 'Товар успешно удален!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Добавляем дополнительный контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление продукта'
        return context