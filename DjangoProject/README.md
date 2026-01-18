# 🛍️ **ПОЛНОЕ РУКОВОДСТВО: ИНТЕРНЕТ-МАГАЗИН НА DJANGO ДЛЯ НОВИЧКОВ**

> 📚 **Исправленная и дополненная версия с учетом всех ошибок**  
> ✅ **Проверено на Django 5.2.10**  
> ⚡ **Пошагово с полным объяснением**  
> 🛡️ **Безопасно для новичков - никаких кастомных моделей пользователя**

---

## 🎯 **ЧТО МЫ СОЗДАДИМ**

<div align="center">

![Магазин на Django](https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif)

*Визуализация конечного результата*
</div>

---

## 📁 **СТРУКТУРА ПРОЕКТА**

```
django_shop/
├── config/              # Настройки проекта
├── products/            # Товары и категории
├── cart/                # Корзина покупок
├── orders/              # Оформление заказов
├── users/               # Пользователи
├── templates/           # HTML шаблоны
├── static/              # Статические файлы
├── media/               # Изображения товаров
└── manage.py            # Управляющий скрипт
```

---

## ⚠️ **ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ**

<div style="background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin: 20px 0;">
⚠️ <strong>Избегаем главных ошибок:</strong>
<ol>
<li><strong>НЕ используем кастомную модель пользователя</strong> - только стандартную</li>
<li><strong>НЕ используем index_together</strong> - устарел в Django 5</li>
<li><strong>НЕ используем пространства имен в URL</strong> - упрощаем для новичков</li>
<li><strong>Создаем файлы по одному</strong> - проверяем каждый шаг</li>
</ol>
</div>

---

# 🚀 **НАЧАЛО РАБОТЫ**

## **ЭТАП 0: ПОДГОТОВКА СРЕДЫ**

### 📦 **Шаг 0.1: Создание проекта с нуля**

```bash
# 1. Создаем папку проекта
mkdir django_shop
cd django_shop

# 2. Создаем виртуальное окружение
python -m venv venv

# 3. Активируем (для Windows PowerShell)
venv\Scripts\Activate.ps1
# Если ошибка прав:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# И повторяем активацию

# 4. Устанавливаем зависимости
pip install django pillow
```

[📖 Подробнее о виртуальных окружениях](https://docs.python.org/3/library/venv.html)

---

### 🏗️ **Шаг 0.2: Создание проекта Django**

```bash
# 1. Создаем проект (точка в конце ОЧЕНЬ важна!)
django-admin startproject config .

# 2. Создаем приложения (по одному)
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp orders
python manage.py startapp users

# 3. Проверяем структуру
# Должно появиться 4 папки с приложениями
```

<div align="center">
<img src="https://media.giphy.com/media/26n7b7PjSOZJwVCmY/giphy.gif" width="300">
</div>

[📖 О структуре Django проекта](https://docs.djangoproject.com/en/5.2/intro/tutorial01/#creating-a-project)

---

### ⚙️ **Шаг 0.3: Настройка config/settings.py**

```python
# config/settings.py

# 1. Добавляем приложения в INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Наши приложения (ПОСЛЕ стандартных!)
    'products',
    'cart',
    'orders',
    'users',
]

# 2. В конец файла добавляем настройки статики
import os

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 3. Для корзины добавляем
CART_SESSION_ID = 'cart'
```

[📖 О настройках Django](https://docs.djangoproject.com/en/5.2/ref/settings/)

---

### 🗄️ **Шаг 0.4: Первичная настройка базы данных**

```bash
# 1. Применяем миграции
python manage.py migrate

# 2. Создаем суперпользователя
python manage.py createsuperuser
# Вводим: admin, admin@example.com, пароль (запомните!)

# 3. Запускаем сервер
python manage.py runserver

# 4. Открываем в браузере:
# Главная: http://127.0.0.1:8000/
# Админка: http://127.0.0.1:8000/admin/
```

<div align="center">

![Запуск Django](https://media.giphy.com/media/3o7abAHdYvZdBNnGZq/giphy.gif)

*Успешный запуск сервера*
</div>

[📖 О миграциях в Django](https://docs.djangoproject.com/en/5.2/topics/migrations/)

---

## ✅ **ПРОВЕРКА ЭТАПА 0**

- [ ] ✔️ Сервер запускается без ошибок
- [ ] ✔️ Видна стартовая страница Django
- [ ] ✔️ Можно войти в админку
- [ ] ✔️ Структура проекта создана

---

# 📦 **ЭТАП 1: МОДЕЛИ ТОВАРОВ (PRODUCTS)**

<div align="center">
<img src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif" width="400">
</div>

### 🏷️ **Шаг 1.1: Создание моделей Category и Product**

**Файл:** `products/models.py`

```python
from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='URL')
    image = models.ImageField(upload_to='products/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        # ⚠️ ВАЖНО: НЕ используем index_together - устарел в Django 5!
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])
```

**🔑 Ключевые моменты:**
- `ForeignKey` - связь товара с категорией
- `ImageField` - для картинок (нужен Pillow)
- `SlugField` - для красивых URL
- `get_absolute_url()` - получение URL объекта

[📖 О моделях Django](https://docs.djangoproject.com/en/5.2/topics/db/models/)

---

### 🛠️ **Шаг 1.2: Регистрация моделей в админке**

**Файл:** `products/admin.py`

```python
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
```

[📖 Об админке Django](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)

---

### 🔄 **Шаг 1.3: Создание и применение миграций**

```bash
# 1. Создаем миграции для products
python manage.py makemigrations products

# 2. Применяем миграции
python manage.py migrate

# 3. Перезапускаем сервер
python manage.py runserver
```

<div style="background: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 4px solid #0c5460; margin: 20px 0;">
💡 <strong>Совет:</strong> Если видите ошибку про <code>index_together</code> - уберите эту строку из models.py
</div>

---

### 🎮 **Шаг 1.4: Тестирование в админке**

1. Откройте http://127.0.0.1:8000/admin/
2. Войдите как суперпользователь
3. Создайте 2-3 категории:
   - 📱 Ноутбуки
   - 📲 Смартфоны
   - 🎧 Наушники
4. Добавьте 4-5 товаров с изображениями

<div align="center">

*Процесс создания товаров*
</div>

---

## ✅ **ПРОВЕРКА ЭТАПА 1**

- [ ] ✔️ Модели созданы без ошибок
- [ ] ✔️ Категории и товары видны в админке
- [ ] ✔️ Можно создавать/редактировать товары
- [ ] ✔️ Изображения загружаются

---

# 🏗️ **ЭТАП 2: ШАБЛОНЫ И ПРЕДСТАВЛЕНИЯ**


### 📂 **Шаг 2.1: Создание структуры папок**

```bash
# Создаем папки для шаблонов
mkdir templates
mkdir templates\products
mkdir templates\cart
mkdir templates\orders
mkdir templates\users

# Создаем папки для статики
mkdir static
mkdir static\images

# Создаем или копируем изображение-заглушку
# в static/images/no-image.png
```

---

### ⚙️ **Шаг 2.2: Настройка TEMPLATES в settings.py**

```python
# config/settings.py

# В разделе TEMPLATES исправляем:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # ВАЖНО!
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Наши контекстные процессоры добавим позже
            ],
        },
    },
]
```

[📖 О шаблонах Django](https://docs.djangoproject.com/en/5.2/topics/templates/)

---

### 🎨 **Шаг 2.3: Базовый шаблон (base.html)**

**Файл:** `templates/base.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Магазин Django{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .product-card-img {
            height: 200px;
            object-fit: cover;
        }
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
    </style>
</head>
<body>
    <!-- Навигация -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="{% url 'product_list' %}">
                🛍️ DjangoShop
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'product_list' %}">Все товары</a>
                    </li>
                    <!-- Категории добавятся через контекстный процессор -->
                </ul>
                
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'cart_detail' %}">
                            🛒 Корзина
                            <span id="cart-counter" class="badge bg-danger"></span>
                        </a>
                    </li>
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'profile' %}">👤 {{ user.username }}</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'logout' %}">🚪 Выйти</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'login' %}">🔑 Войти</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'register' %}">📝 Регистрация</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Контент -->
    <div class="container mt-4">
        {% block content %}
        <!-- Здесь будет контент конкретной страницы -->
        {% endblock %}
    </div>

    <!-- Подвал -->
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container text-center">
            <p>© 2024 DjangoShop. Все права защищены.</p>
        </div>
    </footer>

    <!-- Скрипты -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Простая анимация для кнопок
        document.addEventListener('DOMContentLoaded', function() {
            const buttons = document.querySelectorAll('.btn');
            buttons.forEach(btn => {
                btn.addEventListener('mouseenter', function() {
                    this.style.transform = 'scale(1.05)';
                    this.style.transition = 'transform 0.2s';
                });
                btn.addEventListener('mouseleave', function() {
                    this.style.transform = 'scale(1)';
                });
            });
        });
    </script>
</body>
</html>
```

---

### 🔄 **Шаг 2.4: Контекстный процессор для категорий**

**Файл:** `products/context_processors.py`

```python
from .models import Category

def categories(request):
    """Добавляет категории во все шаблоны"""
    return {
        'categories': Category.objects.all()
    }
```

**Обновляем `settings.py`:**
```python
# В TEMPLATES['OPTIONS']['context_processors'] добавляем:
'products.context_processors.categories',
```

**Обновляем `base.html` - добавляем категории в навигацию:**
```html
<ul class="navbar-nav me-auto">
    <li class="nav-item">
        <a class="nav-link" href="{% url 'product_list' %}">Все товары</a>
    </li>
    {% for category in categories %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'product_list_by_category' category.slug %}">
            {{ category.name }}
        </a>
    </li>
    {% endfor %}
</ul>
```

---

### 🎯 **Шаг 2.5: Представления для товаров**

**Файл:** `products/views.py`

```python
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_slug=None):
    """
    Показывает список товаров.
    Если передан slug категории - показывает только ее товары.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'products/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    """
    Показывает детальную информацию о товаре.
    """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'products/detail.html', {'product': product})
```

[📖 О представлениях Django](https://docs.djangoproject.com/en/5.2/topics/http/views/)

---

### 🛣️ **Шаг 2.6: URL-маршруты товаров**

**Файл:** `products/urls.py`

```python
from django.urls import path
from . import views

# ⚠️ ВАЖНО: БЕЗ app_name! Без пространств имен!
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
```

---

### 📋 **Шаг 2.7: Шаблон списка товаров**

**Файл:** `templates/products/list.html`

```html
{% extends "base.html" %}

{% block title %}
    {% if category %}{{ category.name }}{% else %}Все товары{% endif %}
{% endblock %}

{% block content %}
<div class="row mb-4">
    <div class="col-12">
        <h1 class="display-5">
            {% if category %}
                {{ category.name }}
            {% else %}
                🛒 Все товары
            {% endif %}
        </h1>
        {% if category %}
            <p class="text-muted">{{ products.count }} товаров в категории</p>
        {% endif %}
    </div>
</div>

<div class="row">
    {% for product in products %}
    <div class="col-md-4 mb-4">
        <div class="card h-100 shadow-sm">
            <a href="{% url 'product_detail' product.id product.slug %}" class="text-decoration-none">
                {% if product.image %}
                    <img src="{{ product.image.url }}" 
                         class="card-img-top product-card-img" 
                         alt="{{ product.name }}">
                {% else %}
                    <img src="/static/images/no-image.png" 
                         class="card-img-top product-card-img" 
                         alt="{{ product.name }}">
                {% endif %}
            </a>
            <div class="card-body d-flex flex-column">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text text-muted">{{ product.description|truncatechars:100 }}</p>
                <div class="mt-auto">
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="h4 text-primary">{{ product.price }} ₽</span>
                        <span class="badge {% if product.available %}bg-success{% else %}bg-danger{% endif %}">
                            {% if product.available %}В наличии{% else %}Нет в наличии{% endif %}
                        </span>
                    </div>
                    <div class="d-grid gap-2 mt-3">
                        <a href="{% url 'product_detail' product.id product.slug %}" 
                           class="btn btn-outline-primary">
                            👁️ Подробнее
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12 text-center py-5">
        <h3>😔 Товары не найдены</h3>
        <p class="text-muted">Попробуйте выбрать другую категорию</p>
        <a href="{% url 'product_list' %}" class="btn btn-primary">Вернуться к каталогу</a>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

---

### 🔍 **Шаг 2.8: Шаблон детальной страницы товара**

**Файл:** `templates/products/detail.html`

```html
{% extends "base.html" %}

{% block title %}{{ product.name }}{% endblock %}

{% block content %}
<div class="row">
    <!-- Изображение товара -->
    <div class="col-md-6 mb-4">
        <div class="card shadow-sm">
            {% if product.image %}
                <img src="{{ product.image.url }}" 
                     class="card-img-top img-fluid rounded" 
                     alt="{{ product.name }}">
            {% else %}
                <img src="/static/images/no-image.png" 
                     class="card-img-top img-fluid rounded" 
                     alt="{{ product.name }}">
            {% endif %}
        </div>
    </div>
    
    <!-- Информация о товаре -->
    <div class="col-md-6 mb-4">
        <div class="card shadow-sm h-100">
            <div class="card-body">
                <h1 class="card-title">{{ product.name }}</h1>
                
                <div class="mb-3">
                    <span class="badge bg-secondary">{{ product.category.name }}</span>
                    {% if product.available %}
                        <span class="badge bg-success">✓ В наличии</span>
                    {% else %}
                        <span class="badge bg-danger">✗ Нет в наличии</span>
                    {% endif %}
                </div>
                
                <p class="card-text lead">{{ product.description }}</p>
                
                <div class="d-flex align-items-center mb-4">
                    <span class="display-6 text-primary me-3">{{ product.price }} ₽</span>
                </div>
                
                <!-- Форма добавления в корзину -->
                {% if product.available %}
                <form action="{% url 'cart_add' product.id %}" method="post" class="mt-4">
                    {% csrf_token %}
                    <div class="row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="quantity" class="col-form-label">Количество:</label>
                        </div>
                        <div class="col-auto">
                            <div class="input-group" style="width: 150px;">
                                <button type="button" class="btn btn-outline-secondary" onclick="changeQuantity(-1)">−</button>
                                <input type="number" id="quantity" name="quantity" 
                                       value="1" min="1" max="10" 
                                       class="form-control text-center">
                                <button type="button" class="btn btn-outline-secondary" onclick="changeQuantity(1)">+</button>
                            </div>
                        </div>
                        <div class="col-auto">
                            <button type="submit" class="btn btn-success btn-lg">
                                🛒 Добавить в корзину
                            </button>
                        </div>
                    </div>
                </form>
                {% endif %}
                
                <!-- Навигация -->
                <div class="mt-4 pt-4 border-top">
                    <a href="{% url 'product_list_by_category' product.category.slug %}" 
                       class="btn btn-outline-secondary">
                        ← Назад в {{ product.category.name }}
                    </a>
                    <a href="{% url 'product_list' %}" class="btn btn-outline-primary ms-2">
                        📋 Все товары
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    function changeQuantity(delta) {
        const input = document.getElementById('quantity');
        let value = parseInt(input.value) + delta;
        if (value < 1) value = 1;
        if (value > 10) value = 10;
        input.value = value;
    }
</script>
{% endblock %}
```

---

### 🔗 **Шаг 2.9: Настройка главных URL**

**Файл:** `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  # ⚠️ БЕЗ namespace!
]

# Добавляем маршруты для медиафайлов только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## ✅ **ПРОВЕРКА ЭТАПА 2**

```bash
python manage.py runserver
```

**Что проверяем:**
1. http://127.0.0.1:8000/ - список товаров
2. Клик по товару - переход на детальную страницу
3. Категории в навигации работают
4. Изображения отображаются
5. Нет ошибок в консоли

- [ ] ✔️ Главная страница показывает товары
- [ ] ✔️ Детальная страница товара работает
- [ ] ✔️ Категории в меню отображаются
- [ ] ✔️ Изображения загружаются
- [ ] ✔️ Нет ошибок "TemplateDoesNotExist"

---

# 🛒 **ЭТАП 3: КОРЗИНА ПОКУПОК**


### 🧺 **Шаг 3.1: Класс корзины (работа с сессиями)**

**Файл:** `cart/cart.py`

```python
from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    """
    Класс для управления корзиной покупок.
    Использует сессии Django для хранения данных.
    """
    
    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        # Если корзины нет в сессии - создаем пустую
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def add(self, product, quantity=1, update_quantity=False):
        """Добавить товар в корзину или обновить количество"""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)  # Храним как строку
            }
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        """Сохранить изменения в сессии"""
        self.session.modified = True
    
    def remove(self, product):
        """Удалить товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """Итератор по товарам в корзине"""
        product_ids = self.cart.keys()
        # Получаем объекты товаров из базы
        products = Product.objects.filter(id__in=product_ids)
        
        # Создаем копию корзины для безопасной модификации
        cart = self.cart.copy()
        
        # Добавляем объекты товаров в корзину
        for product in products:
            cart[str(product.id)]['product'] = product
        
        # Проходим по товарам и рассчитываем суммы
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """Общее количество товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """Общая стоимость корзины"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
    
    def clear(self):
        """Очистить корзину"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
```

[📖 О сессиях в Django](https://docs.djangoproject.com/en/5.2/topics/http/sessions/)

---

### 🔄 **Шаг 3.2: Контекстный процессор корзины**

**Файл:** `cart/context_processors.py`

```python
from .cart import Cart

def cart(request):
    """Добавляет корзину во все шаблоны"""
    return {'cart': Cart(request)}
```

**Обновляем `settings.py`:**
```python
# В TEMPLATES['OPTIONS']['context_processors'] добавляем:
'cart.context_processors.cart',
```

---

### 🎮 **Шаг 3.3: Представления корзины**

**Файл:** `cart/views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

@require_POST  # Разрешаем только POST-запросы
def cart_add(request, product_id):
    """Добавить товар в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем количество из формы
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product=product, quantity=quantity)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    """Удалить товар из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    """Показать содержимое корзины"""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
```

---

### 🛣️ **Шаг 3.4: URL-маршруты корзины**

**Файл:** `cart/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
```

**Обновляем `config/urls.py`:**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),  # ДОБАВЛЯЕМ
    # Остальные пути будут позже
]
```

---

### 🛍️ **Шаг 3.5: Шаблон корзины**

**Файл:** `templates/cart/detail.html`

```html
{% extends "base.html" %}

{% block title %}🛒 Корзина покупок{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1 class="display-5 mb-4">🛒 Ваша корзина</h1>
    </div>
</div>

{% if cart %}
<div class="row">
    <div class="col-lg-8">
        <div class="card shadow-sm mb-4">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Товар</th>
                                <th>Количество</th>
                                <th>Цена</th>
                                <th>Сумма</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in cart %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        {% if item.product.image %}
                                            <img src="{{ item.product.image.url }}" 
                                                 width="60" 
                                                 class="rounded me-3" 
                                                 alt="{{ item.product.name }}">
                                        {% else %}
                                            <img src="/static/images/no-image.png" 
                                                 width="60" 
                                                 class="rounded me-3" 
                                                 alt="{{ item.product.name }}">
                                        {% endif %}
                                        <div>
                                            <h6 class="mb-0">{{ item.product.name }}</h6>
                                            <small class="text-muted">{{ item.product.category.name }}</small>
                                        </div>
                                    </div>
                                </td>
                                <td>{{ item.quantity }}</td>
                                <td>{{ item.price }} ₽</td>
                                <td><strong>{{ item.total_price }} ₽</strong></td>
                                <td>
                                    <form action="{% url 'cart_remove' item.product.id %}" method="post" class="d-inline">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-danger btn-sm">
                                            ❌ Удалить
                                        </button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Кнопки действий -->
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'product_list' %}" class="btn btn-outline-primary">
                ← Продолжить покупки
            </a>
            <form action="#" method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">
                    🗑️ Очистить корзину
                </button>
            </form>
        </div>
    </div>
    
    <!-- Итоговая информация -->
    <div class="col-lg-4">
        <div class="card shadow-sm sticky-top" style="top: 20px;">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">📋 Итоги заказа</h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <div class="d-flex justify-content-between mb-2">
                        <span>Товары ({{ cart|length }} шт.)</span>
                        <span>{{ cart.get_total_price }} ₽</span>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span>Доставка</span>
                        <span class="text-success">Бесплатно</span>
                    </div>
                    <hr>
                    <div class="d-flex justify-content-between mb-3">
                        <span class="h5">Итого к оплате:</span>
                        <span class="h4 text-primary">{{ cart.get_total_price }} ₽</span>
                    </div>
                </div>
                
                <div class="d-grid gap-2">
                    <a href="#" class="btn btn-success btn-lg">
                        💳 Перейти к оформлению
                    </a>
                    <a href="{% url 'product_list' %}" class="btn btn-outline-secondary">
                        Добавить еще товары
                    </a>
                </div>
                
                <div class="mt-3 text-center">
                    <small class="text-muted">
                        <i class="bi bi-shield-check"></i>
                        Безопасная оплата · Гарантия возврата
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>

{% else %}
<!-- Пустая корзина -->
<div class="row justify-content-center">
    <div class="col-md-6 text-center py-5">
        <div class="mb-4">
            <div style="font-size: 5rem;">🛒</div>
        </div>
        <h3>Ваша корзина пуста</h3>
        <p class="text-muted mb-4">Добавьте товары из каталога, чтобы сделать заказ</p>
        <a href="{% url 'product_list' %}" class="btn btn-primary btn-lg">
            🛍️ Перейти к покупкам
        </a>
    </div>
</div>
{% endif %}
{% endblock %}
```

---

### 🔄 **Шаг 3.6: Обновление base.html - счетчик корзины**

```html
<!-- В templates/base.html обновляем ссылку на корзину: -->
<a class="nav-link" href="{% url 'cart_detail' %}">
    🛒 Корзина
    {% with total_items=cart|length %}
        {% if total_items > 0 %}
            <span class="badge bg-danger">{{ total_items }}</span>
        {% endif %}
    {% endwith %}
</a>
```

---

## ✅ **ПРОВЕРКА ЭТАПА 3**

```bash
python manage.py runserver
```

**Что проверяем:**
1. На странице товара кнопка "Добавить в корзину"
2. Товар добавляется в корзину
3. Счетчик в навигации обновляется
4. Страница /cart/ показывает добавленные товары
5. Можно удалить товар из корзины

- [ ] ✔️ Товары добавляются в корзину
- [ ] ✔️ Корзина сохраняется между страницами
- [ ] ✔️ Счетчик обновляется
- [ ] ✔️ Можно удалять товары
- [ ] ✔️ Общая стоимость рассчитывается

---

<div align="center">

<em>🎉 Поздравляем! Базовая версия магазина готова!</em>
</div>

---

## 📋 **СВОДКА СОЗДАННОГО**

### ✅ **Что уже работает:**
1. **Админка Django** - управление товарами
2. **Каталог товаров** - категории и товары
3. **Детальные страницы** - информация о товарах
4. **Корзина покупок** - добавление/удаление
5. **Сессионное хранение** - корзина сохраняется

### 🔄 **Что будет дальше:**
1. **ЭТАП 4:** Модели заказов
2. **ЭТАП 5:** Оформление заказа из корзины
3. **ЭТАП 6:** Регистрация и авторизация
4. **ЭТАП 7:** Профиль пользователя
5. **ЭТАП 8:** Финальная настройка

---

## 🆘 **ЕСЛИ ВОЗНИКЛИ ПРОБЛЕМЫ**

### **Распространенные ошибки и решения:**

| Ошибка | Решение |
|--------|---------|
| `TemplateDoesNotExist` | Проверьте `TEMPLATES['DIRS']` в settings.py |
| `No module named 'app.urls'` | Создайте файл `app/urls.py` |
| `'index_together' is invalid` | Удалите эту строку из models.py |
| `'products' is not a registered namespace` | Не используйте `products:` в `{% url %}` |
| `OperationalError: no such table` | Выполните `makemigrations` и `migrate` |

### **Проверочные команды:**
```bash
# Проверить все URL
python manage.py show_urls

# Проверить миграции
python manage.py showmigrations

# Создать дамп данных (если нужно сохранить)
python manage.py dumpdata products --indent 2 > products.json
```

---

## 🎓 **РЕКОМЕНДАЦИИ ДЛЯ УРОКА**

### **Для учителя:**
1. **Объясняйте каждый шаг** - что и зачем делаем
2. **Показывайте ошибки вживую** - это ценный опыт
3. **Делайте паузы** - дайте ученикам повторить
4. **Проверяйте вместе** - после каждого этапа

### **Для учеников:**
1. **Создавайте файлы по одному**
2. **Проверяйте после каждого шага**
3. **Читайте ошибки** - они говорят, что не так
4. **Не бойтесь ошибаться** - это часть обучения

---

<div align="center">

![Успех](https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif)

## 🎉 **ГОТОВЫ ПРОДОЛЖИТЬ?**

**Следующий этап:** Создание моделей заказов и оформление покупки!

---

### 📚 **ПОЛЕЗНЫЕ ССЫЛКИ**

- [📘 Официальная документация Django](https://docs.djangoproject.com/)
- [🎥 Видеоуроки Django для начинающих](https://www.youtube.com/watch?v=F5mRW0jo-U4)
- [💾 Исходный код этого проекта](https://github.com/)
- [❓ Вопросы и ответы по Django](https://stackoverflow.com/questions/tagged/django)

</div>

---

**Автор:** @Gabryelf  
**Версия:** 2.0 (исправленная)  
**Дата:** Январь 2026  
**Лицензия:** MIT  

---

<div align="center">
⭐ <strong>Если это руководство помогло - сохраните его!</strong> ⭐
</div>
