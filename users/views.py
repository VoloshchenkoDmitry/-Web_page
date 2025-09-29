from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Отправка приветственного письма
        user_email = form.cleaned_data.get('email')
        send_mail(
            subject='Добро пожаловать в Skystore!',
            message=f'Вы успешно зарегистрировались в нашем магазине. Добро пожаловать!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )

        messages.success(self.request, 'Регистрация прошла успешно! Проверьте вашу почту.')
        return response


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        messages.success(self.request, f'Добро пожаловать, {self.request.user.email}!')
        return reverse_lazy('catalog:home')


class UserLogoutView(LogoutView):
    def get_next_page(self):
        messages.info(self.request, 'Вы успешно вышли из системы.')
        return reverse_lazy('catalog:home')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return reverse('users:profile')