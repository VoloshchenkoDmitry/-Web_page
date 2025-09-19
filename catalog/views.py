from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно добавить логику обработки формы
        # Например, сохранение в базу данных или отправка email

        messages.success(request, 'Сообщение успешно отправлено!')
        return HttpResponseRedirect('/contacts/')

    return render(request, 'catalog/contacts.html')