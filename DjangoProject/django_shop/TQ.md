# 🗂️ ТРЕБОВАНИЕ К ЗДАЧЕ ПРОЕКТА:

| ПРИЛОЖЕНИЕ | ОЦЕНКА | ВАЖНОСТЬ | ОПИСАНИЕ |
|-----------|------------|------------------|------------------|
| Backend | +1 | Очень важно | Все модули должны работать интегрированно |
| Frontend| +1 | Важно | Шаблоны должны отображаться без ошибок |
| Репозиторий | +1 | Важно | Проект должен быть на Git Hub |
| Модификации | +1 | Дополнитеьно | Сделать несколько методов или проверок - улучшений |
| Документация | +1 | Дополнительно | Должен быть README.md и Issues с описанием модификаций |



# 🛒 **ПОЛНОЕ РУКОВОДСТВО: ИНТЕРНЕТ-МАГАЗИН НА DJANGO**

<div align="center">

![Магазин на Django](https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif)

[Готовые шаблоны проекта](https://github.com/Gabryelf/First_Steps_Python.git)

> " шаг 1 **Перейдите по ссылке** шаг 2 **Скопируйте проект на компьютер и достаньте папку django_shop - в ней модель и фронтенд**
> шаг 3 **Начните проект в Pycharm выбрав папку django_shop в качестве root папки проекта** "

</div>

---

## 📋 **СОДЕРЖАНИЕ**

- [🎯 **Цель проекта**](#-цель-проекта)
- [⚡ **Быстрый старт**](#-быстрый-старт)
- [📁 **Структура проекта**](#-структура-проекта)
- [🚀 **Этап 0: Подготовка среды**](#-этап-0-подготовка-среды)
- [📦 **Этап 1: Модели товаров**](#-этап-1-модели-товаров)
- [🏗️ **Этап 2: Шаблоны и представления**](#️-этап-2-шаблоны-и-представления)
- [🛒 **Этап 3: Корзина покупок**](#-этап-3-корзина-покупок)
- [📦 **Этап 4: Оформление заказов**](#-этап-4-оформление-заказов)
- [👤 **Этап 5: Аутентификация**](#-этап-5-аутентификация)
- [🔧 **Этап 6: Финальная настройка**](#-этап-6-финальная-настройка)
- [⚠️ **Решение проблем**](#️-решение-проблем)

---

## 🎯 **Цель проекта**

> "Лучший способ научиться — это делать. Мы создадим полноценный интернет-магазин с нуля!"

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin: 20px 0;">
<strong>🎯 ЧТО МЫ СОЗДАДИМ:</strong>
<ul>
<li>✅ Каталог товаров с категориями</li>
<li>✅ Корзину покупок на сессиях</li>
<li>✅ Оформление заказов</li>
<li>✅ Регистрацию и авторизацию</li>
<li>✅ Административную панель</li>
</ul>
</div>

---

## ⚡ **БЫСТРЫЙ СТАРТ**

> "Сначала сделай просто работающее, потом сделай красиво"

```bash
# 1. Клонируйте и настройте проект
git clone <репозиторий>
cd django_shop
python -m venv venv
venv\Scripts\activate
pip install django pillow

# 2. Создайте проект и приложения
django-admin startproject config .
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp orders
python manage.py startapp users

# 3. Запустите и проверьте
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📁 **СТРУКТУРА ПРОЕКТА**

```tree
django_shop/
├── config/              # ⚙️ Настройки проекта
├── products/            # 📦 Товары и категории
├── cart/                # 🛒 Корзина покупок
├── orders/              # 📦 Оформление заказов
├── users/               # 👤 Пользователи
├── templates/           # 🎨 HTML шаблоны
├── static/              # 🖼️ Статические файлы
├── media/               # 📸 Изображения товаров
└── manage.py            # 🎮 Управляющий скрипт
```

---

<div style="border-left: 4px solid #4CAF50; padding-left: 15px; margin: 20px 0;">
<strong>💡 СОВЕТ:</strong> Эта структура соответствует лучшим практикам Django и позволяет легко масштабировать проект.
</div>

---

## 🚀 **ЭТАП 0: ПОДГОТОВКА СРЕДЫ**

### 🛠️ **Шаг 0.1: Создание проекта с нуля**

```bash
# Создаем папку и виртуальное окружение
mkdir django_shop && cd django_shop
python -m venv venv

# Активируем (Windows PowerShell)
venv\Scripts\Activate.ps1
# Если ошибка прав:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Устанавливаем зависимости
pip install django pillow
```

[![PyPI](https://img.shields.io/badge/Django-5.2.10-092E20?style=for-the-badge&logo=django)](https://pypi.org/project/Django/)
[![Pillow](https://img.shields.io/badge/Pillow-10.0.0-3776AB?style=for-the-badge&logo=python)](https://pypi.org/project/Pillow/)

> 📚 **Ресурсы:**
> - [Официальная документация Django](https://docs.djangoproject.com/)
> - [Руководство по виртуальным окружениям](https://docs.python.org/3/library/venv.html)
> - [Установка Pillow для работы с изображениями](https://pillow.readthedocs.io/)

---

### ⚙️ **Шаг 0.2: Создание проекта и приложений**

```bash
# Создаем проект (точка в конце ВАЖНА!)
django-admin startproject config .

# Создаем приложения по одному
python manage.py startapp products
python manage.py startapp cart  
python manage.py startapp orders
python manage.py startapp users

# Проверяем структуру
# Должно появиться 4 папки с приложениями
```

> 🎯 **Важно:** Каждое приложение отвечает за свою часть функционала:
> - **products** - товары и категории
> - **cart** - корзина покупок
> - **orders** - оформление заказов
> - **users** - регистрация и авторизация

---

### 🔧 **Шаг 0.3: Настройка config/settings.py**

```python
# config/settings.py - ключевые настройки

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

# ⚠️ ВАЖНО: НЕ добавляем AUTH_USER_MODEL!
# Используем стандартную модель пользователя

# Настройки статических и медиа файлов
import os

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Для корзины
CART_SESSION_ID = 'cart'

# Для аутентификации
LOGIN_REDIRECT_URL = 'product_list'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'product_list'
```

[![Settings](https://img.shields.io/badge/Django_Settings-Important-FF6B6B?style=flat-square)](https://docs.djangoproject.com/en/5.2/ref/settings/)

> 📖 **Подробнее:**
> - [Настройки Django](https://docs.djangoproject.com/en/5.2/ref/settings/)
> - [Работа со статическими файлами](https://docs.djangoproject.com/en/5.2/howto/static-files/)
> - [Настройка медиа файлов](https://docs.djangoproject.com/en/5.2/topics/files/)

---

### 🗄️ **Шаг 0.4: Первичная миграция и суперпользователь**

```bash
# Применяем стандартные миграции
python manage.py migrate

# Создаем суперпользователя для админки
python manage.py createsuperuser
# Вводим: admin, admin@example.com, пароль

# Запускаем сервер для проверки
python manage.py runserver
```

<div align="center">

![Django Admin](https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif)

*Админка Django после входа*
</div>

> ✅ **Проверка:**
> 1. Откройте http://127.0.0.1:8000/ - страница Django
> 2. Откройте http://127.0.0.1:8000/admin/ - войдите
> 3. Убедитесь, что админка доступна

[![Migrations](https://img.shields.io/badge/Migrations-✅-4CAF50?style=flat-square)](https://docs.djangoproject.com/en/5.2/topics/migrations/)

---

## 📦 **ЭТАП 1: МОДЕЛИ ТОВАРОВ**


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

[![Models](https://img.shields.io/badge/Django_Models-📦-2196F3?style=for-the-badge)](https://docs.djangoproject.com/en/5.2/topics/db/models/)

<div style="background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin: 20px 0;">
⚠️ <strong>ИСПРАВЛЕННАЯ ОШИБКА:</strong> В предыдущей версии использовался <code>index_together</code>, который устарел в Django 5.x. Теперь это исправлено!
</div>

> 🔑 **Ключевые моменты:**
> - `ForeignKey` - связь "многие к одному" (товар → категория)
> - `ImageField` - для изображений (требует Pillow)
> - `SlugField` - для ЧПУ (человеко-понятных URL)
> - `get_absolute_url()` - метод для получения URL объекта

---

### 🎮 **Шаг 1.2: Регистрация в админке**

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

[![Admin](https://img.shields.io/badge/Django_Admin-⚡-FF5722?style=flat-square)](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)


---

### 🔄 **Шаг 1.3: Создание и применение миграций**

```bash
# Создаем миграции для products
python manage.py makemigrations products

# Применяем миграции
python manage.py migrate

# Проверяем, что все создалось
python manage.py runserver
```

[![Migrations](https://img.shields.io/badge/Migrations-🔄-9C27B0?style=flat-square)](https://docs.djangoproject.com/en/5.2/topics/migrations/)

> 📊 **Что создается в базе данных:**
> - Таблица `products_category` для категорий
> - Таблица `products_product` для товаров
> - Связи между таблицами

---

### 🎯 **Шаг 1.4: Тестирование в админке**

1. Откройте http://127.0.0.1:8000/admin/
2. В разделе "Products" создайте:
   - 📱 **Категории:** Ноутбуки, Смартфоны, Наушники
   - 💻 **Товары:** 4-5 товаров с изображениями и ценами
   - 🏷️ **Цены:** от 5000 до 100000 рублей

<div style="background: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 4px solid #0c5460; margin: 20px 0;">
💡 <strong>Совет:</strong> Используйте реальные данные для тестирования. Это поможет лучше понять работу приложения.
</div>

---

## 🏗️ **ЭТАП 2: ШАБЛОНЫ И ПРЕДСТАВЛЕНИЯ**


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

> 📁 **Структура шаблонов:**
> ```
> templates/
> ├── base.html              # 🎨 Базовый шаблон
> ├── products/
> │   ├── list.html         # 📋 Список товаров
> │   └── detail.html       # 🔍 Детальная страница
> ├── cart/
> │   └── detail.html       # 🛒 Корзина покупок
> ├── orders/
> │   ├── create.html       # 📝 Оформление заказа
> │   └── created.html      # ✅ Подтверждение заказа
> └── users/
>     ├── login.html        # 🔑 Вход
>     ├── register.html     # 📝 Регистрация
>     └── profile.html      # 👤 Профиль пользователя
> ```

[![Templates](https://img.shields.io/badge/Django_Templates-🎨-FF9800?style=flat-square)](https://docs.djangoproject.com/en/5.2/topics/templates/)

---

### ⚙️ **Шаг 2.2: Настройка шаблонов в settings.py**

```python
# config/settings.py - настройка TEMPLATES

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
                'products.context_processors.categories',  # Добавим позже
                'cart.context_processors.cart',           # Добавим позже
            ],
        },
    },
]
```

---

### 🎨 **Шаг 2.3: Работа с шаблонами HTML**

> 📝 **Важно:** Мы не пишем полный код шаблонов здесь, а описываем их структуру и ключевые моменты.

**Шаблоны, которые нужно создать:**

| Шаблон | Путь | Назначение |
|--------|------|------------|
| **Базовый шаблон** | `templates/base.html` | Основная разметка, навигация |
| **Список товаров** | `templates/products/list.html` | Отображение товаров сеткой |
| **Детальная страница** | `templates/products/detail.html` | Полная информация о товаре |

<div style="border-left: 4px solid #2196F3; padding-left: 15px; margin: 20px 0;">
<strong>💡 Ключевые теги Django для шаблонов:</strong>
<ul>
<li><code>{% extends "base.html" %}</code> - наследование шаблонов</li>
<li><code>{% block content %}{% endblock %}</code> - блоки контента</li>
<li><code>{% url 'product_list' %}</code> - генерация URL (БЕЗ namespace!)</li>
<li><code>{% for product in products %}</code> - циклы</li>
<li><code>{{ product.name }}</code> - вывод переменных</li>
<li><code>{% if user.is_authenticated %}</code> - условия</li>
</ul>
</div>

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

> 🎯 **Зачем это нужно:** Чтобы категории были доступны в навигации на всех страницах без явной передачи в каждое представление.

---

### 🎯 **Шаг 2.5: Представления для товаров**

**Файл:** `products/views.py`

```python
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_slug=None):
    """Отображает список товаров (всех или по категории)"""
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
    """Отображает детальную информацию о товаре"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'products/detail.html', {'product': product})
```

[![Views](https://img.shields.io/badge/Django_Views-🎯-4CAF50?style=flat-square)](https://docs.djangoproject.com/en/5.2/topics/http/views/)

---

### 🛣️ **Шаг 2.6: URL-маршруты товаров**

**Файл:** `products/urls.py`

```python
from django.urls import path
from . import views

# ⚠️ ВАЖНО: БЕЗ app_name! Без пространств имен для упрощения!
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
```

> 🔗 **Объяснение URL паттернов:**
> - `''` - главная страница со всеми товарами
> - `'<slug:category_slug>/'` - товары конкретной категории
> - `'<int:id>/<slug:slug>/'` - детальная страница товара

---

### 🔗 **Шаг 2.7: Настройка главных URL**

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

<div style="background: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50; margin: 20px 0;">
✅ <strong>ПРОВЕРКА:</strong> После этого этапа у вас должна работать главная страница со списком товаров!
</div>

---

## 🛒 **ЭТАП 3: КОРЗИНА ПОКУПОК**


### 🧺 **Шаг 3.1: Класс корзины (сессионная)**

**Файл:** `cart/cart.py`

```python
from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    """Класс для управления корзиной покупок в сессиях"""
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def add(self, product, quantity=1):
        """Добавить товар в корзину"""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
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
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
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

[![Sessions](https://img.shields.io/badge/Django_Sessions-🔐-673AB7?style=flat-square)](https://docs.djangoproject.com/en/5.2/topics/http/sessions/)

> 🔒 **Как работает:**
> - Корзина хранится в сессии пользователя
> - Каждый товар имеет ID, количество и цену
> - Сессия сохраняется между запросами
> - Нет необходимости в модели БД для корзины

---

### 🔄 **Шаг 3.2: Контекстный процессор корзины**

**Файл:** `cart/context_processors.py`

```python
from .cart import Cart

def cart(request):
    """Добавляет корзину во все шаблоны"""
    return {'cart': Cart(request)}
```

> 🎯 **Результат:** Теперь `{{ cart }}` доступен во всех шаблонах

---

### 🎮 **Шаг 3.3: Представления корзины**

**Файл:** `cart/views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

@require_POST  # Только POST-запросы
def cart_add(request, product_id):
    """Добавить товар в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
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
    # orders и users добавятся позже
]
```

---

### 🛍️ **Шаг 3.5: Шаблон корзины (основные моменты)**

**Файл:** `templates/cart/detail.html`

**Ключевые элементы:**
1. Таблица с товарами в корзине
2. Форма удаления товаров (POST запросы)
3. Подсчет общей стоимости
4. Ссылки на продолжение покупок
5. Отображение пустой корзины

> 💡 **Совет по реализации:**
> - Используйте Bootstrap таблицы для красивого отображения
> - Добавьте иконки для кнопок удаления
> - Реализуйте подсчет итоговой суммы
> - Сделайте адаптивный дизайн для мобильных устройств

<div align="center">

![Shopping Cart](https://media.giphy.com/media/3o7TKr3r78bNcLtBna/giphy.gif)

*Работа корзины покупок*
</div>

---

## 📦 **ЭТАП 4: ОФОРМЛЕНИЕ ЗАКАЗОВ**

<div align="center">
<img src="https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif" width="400">
</div>

### 📝 **Шаг 4.1: Модели заказа**

**Файл:** `orders/models.py`

```python
from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    """Модель заказа"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                             null=True, blank=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f'Заказ {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    """Товар в заказе"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, 
                              verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', 
                                on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
```

[![Models](https://img.shields.io/badge/Order_Models-📝-009688?style=flat-square)](https://docs.djangoproject.com/en/5.2/topics/db/examples/many_to_one/)

> 🔗 **Связи моделей:**
> - `Order` связан с `User` (необязательно)
> - `OrderItem` связан с `Order` и `Product`
> - Один заказ может содержать несколько товаров

---

### 🔄 **Шаг 4.2: Миграции заказов**

```bash
# Создаем миграции
python manage.py makemigrations orders

# Применяем миграции
python manage.py migrate

# Проверяем создание таблиц
python manage.py dbshell
# В SQLite: .tables
```

---

### 📋 **Шаг 4.3: Форма заказа**

**Файл:** `orders/forms.py`

```python
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    """Форма оформления заказа"""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 
                  'address', 'postal_code', 'city']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
```

[![Forms](https://img.shields.io/badge/Django_Forms-📋-795548?style=flat-square)](https://docs.djangoproject.com/en/5.2/topics/forms/)

---

### 🎮 **Шаг 4.4: Представление оформления заказа**

**Файл:** `orders/views.py`

```python
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    """Оформление заказа из корзины"""
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            # Привязываем заказ к пользователю, если он авторизован
            if request.user.is_authenticated:
                order.user = request.user
            
            order.save()
            
            # Создаем позиции заказа
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Очищаем корзину
            cart.clear()
            
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})
```

---

### 🛣️ **Шаг 4.5: URL-маршруты заказов**

**Файл:** `orders/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
]
```

**Обновляем `config/urls.py`:**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),  # ДОБАВЛЯЕМ
]
```

---

## 👤 **ЭТАП 5: АУТЕНТИФИКАЦИЯ**

<div align="center">
<img src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif" width="400">
</div>

### 📝 **Шаг 5.1: Форма регистрации**

**Файл:** `users/forms.py`

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    """Расширенная форма регистрации с email"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
```

[![Auth](https://img.shields.io/badge/Django_Auth-👤-FF4081?style=flat-square)](https://docs.djangoproject.com/en/5.2/topics/auth/)

---

### 🎮 **Шаг 5.2: Представления пользователей**

**Файл:** `users/views.py`

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from orders.models import Order

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """Профиль пользователя с историей заказов"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'orders': orders})
```

---

### 🛣️ **Шаг 5.3: URL-маршруты пользователей**

**Файл:** `users/urls.py`

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='product_list'
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
]
```

**Обновляем `config/urls.py`:**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),  # ДОБАВЛЯЕМ
]
```

---

## 🔧 **ЭТАП 6: ФИНАЛЬНАЯ НАСТРОЙКА**

<div align="center">
<img src="https://media.giphy.com/media/3o7TKsQ8gTp3WqXqjq/giphy.gif" width="400">
</div>

### 🎨 **Шаг 6.1: Создание базовых шаблонов**

**Структура шаблонов для реализации:**

| Шаблон | Путь | Описание |
|--------|------|----------|
| **Базовый шаблон** | `templates/base.html` | Основная разметка с навигацией |
| **Логин** | `templates/users/login.html` | Форма входа |
| **Регистрация** | `templates/users/register.html` | Форма регистрации |
| **Профиль** | `templates/users/profile.html` | История заказов |
| **Оформление заказа** | `templates/orders/create.html` | Форма заказа |
| **Подтверждение** | `templates/orders/created.html` | Успешное оформление |

> 💡 **Советы по дизайну:**
> - Используйте Bootstrap 5 для стилизации
> - Добавьте иконки для наглядности
> - Сделайте адаптивный дизайн
> - Используйте карточки для товаров

---

### 🧪 **Шаг 6.2: Тестирование всего функционала**

```bash
# Запускаем сервер
python manage.py runserver
```

**Проверяем по порядку:**

1. **Главная страница:** http://127.0.0.1:8000/
   - Проверяем список товаров
   - Переход по категориям
   - Детальные страницы товаров

2. **Корзина:** http://127.0.0.1:8000/cart/
   - Добавление товаров в корзину
   - Удаление из корзины
   - Подсчет общей суммы

3. **Аутентификация:**
   - Регистрация: http://127.0.0.1:8000/users/register/
   - Вход: http://127.0.0.1:8000/users/login/
   - Профиль: http://127.0.0.1:8000/users/profile/

4. **Заказы:**
   - Оформление: http://127.0.0.1:8000/orders/create/
   - Проверка в админке

5. **Админка:** http://127.0.0.1:8000/admin/
   - Управление товарами
   - Просмотр заказов
   - Управление пользователями

---

### 🐛 **Шаг 6.3: Решение распространенных проблем**

<div style="background: #ffebee; padding: 15px; border-radius: 5px; border-left: 4px solid #f44336; margin: 20px 0;">
⚠️ <strong>ЧАСТЫЕ ОШИБКИ И РЕШЕНИЯ</strong>
</div>

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `TemplateDoesNotExist` | Неправильный путь к шаблонам | Проверить `TEMPLATES['DIRS']` в settings.py |
| `No module named 'app.urls'` | Файл urls.py не создан | Создать файл `app/urls.py` |
| `'index_together' is invalid` | Устаревший атрибут в Django 5 | Удалить `index_together` из models.py |
| `'products' is not a registered namespace` | Использование namespace в URL | Использовать `{% url 'product_list' %}` вместо `{% url 'products:product_list' %}` |
| `OperationalError: no such table` | Миграции не применены | Выполнить `makemigrations` и `migrate` |

---

## ✅ **ЧЕК-ЛИСТ ГОТОВНОСТИ ПРОЕКТА**

<div align="center">

![Checklist](https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif)

</div>

### 🎯 **БАЗОВЫЙ ФУНКЦИОНАЛ:**
- [ ] ✅ Сервер запускается без ошибок
- [ ] ✅ Админка доступна и работает
- [ ] ✅ Категории и товары отображаются
- [ ] ✅ Можно перейти на детальную страницу товара

### 🛒 **КОРЗИНА:**
- [ ] ✅ Товары добавляются в корзину
- [ ] ✅ Корзина сохраняется между страницами
- [ ] ✅ Можно удалять товары из корзины
- [ ] ✅ Счетчик в навигации работает

### 👤 **ПОЛЬЗОВАТЕЛИ:**
- [ ] ✅ Регистрация работает
- [ ] ✅ Вход и выход работают
- [ ] ✅ Профиль показывает историю заказов

### 📦 **ЗАКАЗЫ:**
- [ ] ✅ Оформление заказа из корзины
- [ ] ✅ Заказы сохраняются в базе данных
- [ ] ✅ Корзина очищается после заказа
- [ ] ✅ Заказы видны в админке

---

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 10px; color: white; text-align: center; margin: 30px 0;">
<h2>🎉 ПОЗДРАВЛЯЮ! ВЫ СОЗДАЛИ ИНТЕРНЕТ-МАГАЗИН НА DJANGO!</h2>
<p>Теперь у вас есть полноценный рабочий прототип, который можно развивать дальше.</p>
</div>

---

## 🚀 **ДОПОЛНИТЕЛЬНЫЕ ВОЗМОЖНОСТИ**

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0;">

<div style="background: #E3F2FD; padding: 20px; border-radius: 10px;">
<h3>📊 Пагинация товаров</h3>
<p>Добавить постраничную навигацию для каталога</p>
<code>from django.core.paginator import Paginator</code>
</div>

<div style="background: #F3E5F5; padding: 20px; border-radius: 10px;">
<h3>🔍 Поиск по товарам</h3>
<p>Реализовать поиск по названию и описанию</p>
<code>Product.objects.filter(name__icontains=query)</code>
</div>

<div style="background: #E8F5E9; padding: 20px; border-radius: 10px;">
<h3>⭐ Отзывы и рейтинги</h3>
<p>Добавить возможность оставлять отзывы</p>
<code>class Review(models.Model):</code>
</div>

<div style="background: #FFF3E0; padding: 20px; border-radius: 10px;">
<h3>🎁 Скидки и промокоды</h3>
<p>Система скидок и промокодов</p>
<code>class Discount(models.Model):</code>
</div>

</div>

---

## 📚 **РЕКОМЕНДУЕМЫЕ РЕСУРСЫ**

<div align="center">

[![Django Docs](https://img.shields.io/badge/Django_Documentation-092E20?style=for-the-badge&logo=django&logoColor=white)](https://docs.djangoproject.com/)
[![Django Girls](https://img.shields.io/badge/Django_Girls_Tutorial-F37626?style=for-the-badge&logo=django&logoColor=white)](https://tutorial.djangogirls.org/)
[![MDN Django](https://img.shields.io/badge/MDN_Django_Tutorial-000000?style=for-the-badge&logo=mdnwebdocs&logoColor=white)](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)
[![Real Python](https://img.shields.io/badge/Real_Python_Django-FF6B6B?style=for-the-badge&logo=python&logoColor=white)](https://realpython.com/tutorials/django/)

</div>

---

<div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 2px solid #eee;">
<p><strong>🎓 Учебное пособие по Django</strong></p>
<p>Версия 3.0 • Обновлено: Январь 2026 • Автор: @Gabryelf</p>
<p>Если это руководство помогло — поделитесь с коллегами! 🚀</p>
</div>

---

<div align="center">
<img src="https://media.giphy.com/media/26n7b7PjSOZJwVCmY/giphy.gif" width="200">
<br>
<strong>Удачи в разработке! 🚀</strong>
</div>
