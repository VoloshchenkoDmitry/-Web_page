from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Contact
from .forms import ProductForm


def home(request):
    product_list = Product.objects.all().order_by('-created_at')
    paginator = Paginator(product_list, 6)  # 6 товаров на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Вывод в консоль для дополнительного задания
    print("Последние 5 продуктов:")
    for product in product_list[:5]:
        print(f"- {product.name} ({product.price})")

    context = {
        'page_obj': page_obj
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    contact_info = Contact.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Обработка формы
        messages.success(request, 'Сообщение успешно отправлено!')
        return HttpResponseRedirect('/contacts/')

    context = {
        'contact_info': contact_info
    }
    return render(request, 'catalog/contacts.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('catalog:home')
    else:
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {'form': form})