from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product, Contact


def home(request):
    latest_products = Product.objects.all().order_by('-created_at')[:5]
    print("Последние 5 продуктов:")
    for product in latest_products:
        print(f"- {product.name} ({product.price})")

    context = {
        'latest_products': latest_products
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    contact_info = Contact.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно добавить логику обработки формы
        print(f"Получено сообщение от {name}: {message}")

        messages.success(request, 'Сообщение успешно отправлено!')
        return HttpResponseRedirect('/contacts/')

    context = {
        'contact_info': contact_info
    }
    return render(request, 'catalog/contacts.html', context)