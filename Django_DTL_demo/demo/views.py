from django.shortcuts import render


def home(request):
    # Создаем данные для шаблона
    context = {
        'user_name': 'Serj',
        'age': 25,
        'items': ['Яблоко', 'Банан', 'Апельсин'],
        'price': 99.99,
    }
    return render(request, 'home.html', context)


def about(request):
    context = {
        'company': 'Top Academy',
        'year': 2026,
    }
    return render(request, 'about.html', context)


def products(request):
    products_list = [
        {'name': 'Телефон', 'price': 1000},
        {'name': 'Ноутбук', 'price': 2000},
        {'name': 'Планшет', 'price': 500},
    ]
    return render(request, 'products.html', {'products': products_list})