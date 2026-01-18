from django.shortcuts import render
from datetime import datetime


# Главная страница
def home(request):
    return render(request, 'demo/home.html')


# Страница блоков
def blocks_demo(request):
    context = {
        'page_title': 'Блоки в Django',
        'current_time': datetime.now(),
    }
    return render(request, 'demo/blocks.html', context)


# Страница переменных
def variables_demo(request):
    context = {
        'string_var': 'Привет, Django!',
        'number_var': 42,
        'float_var': 3.14159,
        'list_var': ['Python', 'Django', 'HTML', 'CSS'],
        'dict_var': {
            'name': 'Иван',
            'age': 25,
            'city': 'Москва'
        },
        'bool_var': True,
        'none_var': None,
        'current_date': datetime.now(),
    }
    return render(request, 'demo/variables.html', context)


# Страница фильтров
def filters_demo(request):
    context = {
        'long_text': 'Это очень длинный текст, который нужно обрезать для демонстрации работы фильтров в Django Template Language.',
        'html_text': '<script>alert("опасно!")</script><p>Безопасный текст</p>',
        'price': 1234.5678,
        'users': [
            {'name': 'Алексей', 'score': 95},
            {'name': 'Мария', 'score': 88},
            {'name': 'Иван', 'score': 92},
            {'name': 'Ольга', 'score': 78},
        ],
        'numbers': [3, 1, 4, 1, 5, 9, 2, 6, 5],
        'sentence': 'quick brown fox jumps over the lazy dog',
    }
    return render(request, 'demo/filters.html', context)


# Страница тегов
def tags_demo(request):
    context = {
        'items': ['Яблоко', 'Банан', 'Апельсин', 'Груша', 'Киви'],
        'posts': [
            {'title': 'Первая статья', 'published': True, 'views': 150},
            {'title': 'Вторая статья', 'published': False, 'views': 0},
            {'title': 'Третья статья', 'published': True, 'views': 300},
            {'title': 'Четвертая статья', 'published': True, 'views': 75},
        ],
        'user': {'name': 'Админ', 'is_admin': True},
        'empty_list': [],
        'score': 85,
    }
    return render(request, 'demo/tags.html', context)


# Страница наследования
def inheritance_demo(request):
    return render(request, 'demo/inheritance.html')


# Страница включений
def includes_demo(request):
    return render(request, 'demo/includes.html')
