# 🎯 Минималистичное руководство по Django шаблонам

## 📚 Введение

**Django Template Language (DTL)** - это система, которая позволяет вставлять динамические данные в HTML. Представьте, что у вас есть письмо-шаблон, где меняется только имя получателя - DTL делает именно это!

---

## 🚀 Часть 1: Быстрый старт

### 1.1 Создаем проект
```bash
# В PyCharm Terminal:
mkdir django_templates_simple
cd django_templates_simple

python -m venv venv
venv\Scripts\activate  # Для Windows
pip install django

django-admin startproject simpletemplates .
python manage.py startapp demo
```

### 1.2 Базовая настройка
**В `simpletemplates/settings.py`:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo',  # ⬅️ наше приложение
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ⬅️ ВАЖНО!
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

---

## 📦 Часть 2: Наследование шаблонов (самое важное!)

### 2.1 Создаем базовый шаблон
**Создаем файл `templates/base.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Мой сайт{% endblock %}</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .header { background: blue; color: white; padding: 15px; }
        .content { padding: 20px; }
        .footer { background: gray; color: white; padding: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Шапка сайта</h1>
    </div>
    
    <div class="content">
        {% block content %}
        <!-- Сюда вставляется контент страниц -->
        {% endblock %}
    </div>
    
    <div class="footer">
        <p>Подвал сайта</p>
    </div>
</body>
</html>
```

**Объяснение:**
- `{% block %}` - определяет место, которое можно менять
- `{% endblock %}` - конец блока
- `title` и `content` - имена блоков

---

## 🔤 Часть 3: Переменные

### 3.1 Создаем View
**В `demo/views.py`:**
```python
from django.shortcuts import render

def home(request):
    # Создаем данные для шаблона
    context = {
        'user_name': 'Иван',
        'age': 25,
        'items': ['Яблоко', 'Банан', 'Апельсин'],
        'price': 99.99,
    }
    return render(request, 'home.html', context)

def about(request):
    context = {
        'company': 'Моя компания',
        'year': 2024,
    }
    return render(request, 'about.html', context)
```

### 3.2 Создаем шаблон с переменными
**Создаем `templates/home.html`:**
```html
{% extends 'base.html' %}

{% block title %}Главная страница{% endblock %}

{% block content %}
<h2>Привет, {{ user_name }}!</h2>

<p>Тебе {{ age }} лет.</p>
<p>Товар стоит {{ price }} руб.</p>

<h3>Список продуктов:</h3>
<ul>
    <li>{{ items.0 }}</li>  <!-- Первый элемент -->
    <li>{{ items.1 }}</li>  <!-- Второй элемент -->
    <li>{{ items.2 }}</li>  <!-- Третий элемент -->
</ul>
{% endblock %}
```

**Что мы сделали:**
1. `{% extends 'base.html' %}` - наследуем базовый шаблон
2. `{{ user_name }}` - выводим переменную
3. `{{ items.0 }}` - обращаемся к элементу списка по индексу

---

## 🎛️ Часть 4: Фильтры (преобразование данных)

### 4.1 Простые фильтры
**Создаем `templates/about.html`:**
```html
{% extends 'base.html' %}

{% block title %}О нас{% endblock %}

{% block content %}
<h2>О компании {{ company|upper }}</h2>  <!-- upper - ВЕРХНИЙ РЕГИСТР -->

<p>Год основания: {{ year }}</p>

<!-- Примеры фильтров: -->
<p>Привет в верхнем регистре: {{ "привет"|upper }}</p>
<p>ПРИВЕТ в нижнем регистре: {{ "ПРИВЕТ"|lower }}</p>
<p>Первая заглавная: {{ "привет мир"|capfirst }}</p>
<p>Слов стало: {{ "привет мир"|wordcount }}</p>
<p>Символов: {{ "привет"|length }}</p>
<p>Только первые 5 символов: {{ "длинный текст"|truncatechars:5 }}</p>
{% endblock %}
```

**Основные фильтры:**
- `|upper` - в верхний регистр
- `|lower` - в нижний регистр  
- `|capfirst` - первая буква заглавная
- `|length` - длина строки или списка
- `|truncatechars:N` - обрезать до N символов

---

## 🔄 Часть 5: Теги (логика в шаблонах)

### 5.1 Цикл for
**В `demo/views.py` добавляем:**
```python
def products(request):
    products_list = [
        {'name': 'Телефон', 'price': 1000},
        {'name': 'Ноутбук', 'price': 2000},
        {'name': 'Планшет', 'price': 500},
    ]
    return render(request, 'products.html', {'products': products_list})
```

**Создаем `templates/products.html`:**
```html
{% extends 'base.html' %}

{% block title %}Товары{% endblock %}

{% block content %}
<h2>Наши товары:</h2>

<table border="1">
    <tr>
        <th>Название</th>
        <th>Цена</th>
    </tr>
    
    {% for product in products %}
    <tr>
        <td>{{ product.name }}</td>
        <td>{{ product.price }} руб.</td>
    </tr>
    {% endfor %}
</table>

<p>Всего товаров: {{ products|length }}</p>
{% endblock %}
```

### 5.2 Условие if
**Создаем `templates/user.html`:**
```html
{% extends 'base.html' %}

{% block title %}Пользователь{% endblock %}

{% block content %}
{% if user_name %}
    <h2>Привет, {{ user_name }}!</h2>
{% else %}
    <h2>Привет, гость!</h2>
{% endif %}

{% if age >= 18 %}
    <p>Вам доступен взрослый контент</p>
{% else %}
    <p>Вам доступен детский контент</p>
{% endif %}
{% endblock %}
```

---

## 🧩 Часть 6: Включение шаблонов

### 6.1 Создаем маленький шаблон
**Создаем `templates/includes/menu.html`:**
```html
<ul>
    <li><a href="/">Главная</a></li>
    <li><a href="/about/">О нас</a></li>
    <li><a href="/products/">Товары</a></li>
</ul>
```

### 6.2 Включаем его
**Обновляем `templates/base.html`:**
```html
<!-- Внутри тега body: -->
<div class="header">
    <h1>Шапка сайта</h1>
    {% include 'includes/menu.html' %}  <!-- ⬅️ ВКЛЮЧАЕМ -->
</div>
```

---

## 🛣️ Часть 7: Настройка URL

### 7.1 В `demo/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
]
```

### 7.2 В `simpletemplates/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('demo.urls')),
]
```

---

## 🚀 Часть 8: Запуск и тестирование

### 8.1 Создаем все файлы:
```
django_templates_simple/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── products.html
│   ├── user.html
│   └── includes/
│       └── menu.html
├── demo/
│   ├── views.py
│   └── urls.py
├── simpletemplates/
├── manage.py
└── venv/
```

### 8.2 Запускаем:
```bash
python manage.py migrate
python manage.py runserver
```

**Открываем в браузере:**
- http://127.0.0.1:8000/ - главная
- http://127.0.0.1:8000/about/ - о нас
- http://127.0.0.1:8000/products/ - товары

---

## 📚 Шпаргалка для студентов

### 🎯 4 главные вещи:

#### 1. **Переменные** - вывод данных
```html
{{ имя_переменной }}
{{ список.0 }}        <!-- элемент списка -->
{{ словарь.ключ }}    <!-- значение словаря -->
```

#### 2. **Фильтры** - преобразование
```html
{{ текст|upper }}     <!-- ВЕРХНИЙ РЕГИСТР -->
{{ текст|lower }}     <!-- нижний регистр -->
{{ список|length }}   <!-- количество -->
{{ текст|slice:":5" }}<!-- первые 5 символов -->
```

#### 3. **Теги** - логика
```html
{% for item in list %}   <!-- цикл -->
{% if условие %}         <!-- условие -->
{% include "шаблон" %}   <!-- включение -->
{% extends "база" %}     <!-- наследование -->
```

#### 4. **Наследование** - основа
```html
<!-- base.html (родитель) -->
{% block content %}{% endblock %}

<!-- page.html (ребенок) -->
{% extends "base.html" %}
{% block content %}Мой контент{% endblock %}
```

### 🎯 Простой алгоритм создания страницы:

1. **Создайте view** (функцию в `views.py`)
```python
def page(request):
    data = {'var': 'значение'}
    return render(request, 'page.html', data)
```

2. **Создайте шаблон** (файл в `templates/`)
```html
{% extends 'base.html' %}
{% block content %}{{ var }}{% endblock %}
```

3. **Добавьте URL** (в `urls.py`)
```python
path('page/', views.page, name='page')
```

---

## 🎯 5 минут на понимание:

### Вопрос: Чем отличаются эти три конструкции?

1. **{{ переменная }}** - Показывает значение
   ```html
   {{ "Привет" }} → Привет
   ```

2. **{% тег %}** - Выполняет действие
   ```html
   {% if True %}Да{% endif %} → Да
   ```

3. **{# комментарий #}** - Невидимый текст
   ```html
   {# Это не покажется #} → (ничего)
   ```

### Аналогия из жизни:

**Шаблон Django** = **Письмо-шаблон**
- `{{ имя }}` = Место для имени получателя
- `{% if день_рождения %}` = Проверка: если день рождения
- `{% for подарок in подарки %}` = Перебор всех подарков
- `|upper` = Написать заглавными буквами

---

## 🛠️ Часть 9: Практическое задание

### Создайте страницу с погодой:

1. **View:**
```python
def weather(request):
    cities = [
        {'name': 'Москва', 'temp': '+15°C'},
        {'name': 'Санкт-Петербург', 'temp': '+12°C'},
        {'name': 'Сочи', 'temp': '+20°C'},
    ]
    return render(request, 'weather.html', {'cities': cities})
```

2. **Шаблон `weather.html`:**
```html
{% extends 'base.html' %}
{% block content %}
<h2>Погода в городах</h2>
<ul>
{% for city in cities %}
    <li>{{ city.name }}: {{ city.temp }}</li>
{% endfor %}
</ul>
{% endblock %}
```

3. **URL:**
```python
path('weather/', views.weather, name='weather')
```

---

## ✅ Итог: Что вы узнали?

### Основы шаблонов Django:
1. ✅ **Наследование** - один базовый шаблон для всех страниц
2. ✅ **Переменные** - вывод данных `{{ ... }}`
3. ✅ **Фильтры** - преобразование данных `|filter`
4. ✅ **Теги** - логика в шаблонах `{% ... %}`
5. ✅ **Включения** - повторное использование кода

### Самое важное:
- **Начинайте всегда с `{% extends 'base.html' %}`**
- **Данные приходят из view в шаблон**
- **`{{ }}` для вывода, `{% %}` для действий**
- **Фильтры меняют как данные выглядят**

### Для запоминания:
```html
{% extends 'base.html' %}  <!-- Наследование -->
{% block content %}        <!-- Блок контента -->
    {{ переменная|фильтр }}  <!-- Вывод с фильтром -->
    {% if условие %}        <!-- Условие -->
    {% for item in list %}  <!-- Цикл -->
    {% include "шаблон" %}  <!-- Включение -->
{% endblock %}
```

---

## 🎉 Поздравляю! Вы освоили основы шаблонов Django!

**Теперь вы можете:**
- ✅ Создавать страницы с динамическим контентом
- ✅ Использовать наследование для единого дизайна
- ✅ Применять фильтры для форматирования данных
- ✅ Добавлять логику с помощью тегов
- ✅ Создавать модульные компоненты

**Далее изучайте:**
1. Формы Django
2. Админ-панель
3. Базы данных
4. Пользовательская аутентификация

**Помните:** Шаблоны - это "лицо" вашего сайта. Чем они чище и понятнее, тем лучше! 🚀
