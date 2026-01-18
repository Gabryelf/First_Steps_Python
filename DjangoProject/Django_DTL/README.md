# 🎨 Django Шаблонизация: Полное руководство по блокам и переменным

## 📚 Введение в Django Template Language (DTL)

### 🎯 Что такое шаблонизатор Django?
**Django Template Language (DTL)** — это специальный язык, который позволяет вставлять динамические данные в HTML. Представьте, что у вас есть письмо, где нужно менять только имя получателя — шаблонизатор делает именно это!

**Зачем нужен шаблонизатор?**
- 🎨 **Разделение логики и дизайна** — программисты и дизайнеры не мешают друг другу
- 🔄 **Повторное использование** — один шаблон для многих страниц
- 🛡️ **Безопасность** — автоматическая защита от XSS-атак
- 📦 **Наследование** — как в ООП, но для HTML

### 🎨 Что мы будем создавать?
Мы создадим **проект-демонстрацию** всех возможностей шаблонизации Django:
- 📁 Наследование шаблонов
- 📦 Блоки и их переопределение
- 🔤 Переменные и фильтры
- 🔄 Теги и циклы
- 🧩 Включение шаблонов
- 📝 Пользовательские фильтры и теги

---

## 📦 Часть 1: Создание проекта для изучения шаблонизации

### 🖥️ 1.1 Подготовка проекта
```bash
# Создаем папку проекта
mkdir django_templates_demo
cd django_templates_demo

# Создаем виртуальное окружение
python -m venv venv

# Активируем (Windows)
venv\Scripts\activate

# Устанавливаем Django
pip install django
```

### 🏗️ 1.2 Создание проекта и приложения
```bash
# Создаем проект (обратите внимание на точку!)
django-admin startproject templatedemo .

# Создаем приложение
python manage.py startapp demo

# Проверяем структуру
dir
# Должно быть: manage.py, templatedemo/, venv/
```

### ⚙️ 1.3 Настройка проекта
**Открываем `templatedemo/settings.py`:**

```python
# Добавляем приложение
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo',  # ⬅️ НАШЕ ПРИЛОЖЕНИЕ
]

# ⭐ ВАЖНО ДЛЯ ШАБЛОНОВ!
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # ⬅️ ГЛОБАЛЬНЫЕ ШАБЛОНЫ
            BASE_DIR / 'demo/templates',  # ⬅️ ШАБЛОНЫ ПРИЛОЖЕНИЯ
        ],
        'APP_DIRS': True,  # Искать шаблоны в папках приложений
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

# Статические файлы
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Язык
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
```

### 📁 1.4 Создание структуры папок
**В PyCharm создаем структуру:**

```
django_templates_demo/
├── templates/          # Глобальные шаблоны ⭐
├── demo/templates/demo/ # Шаблоны приложения
├── static/            # CSS, JS, изображения
└── demo/templatetags/ # Пользовательские теги ⭐
```

**Как создать:**
1. ПКМ на проекте → **New → Directory**
2. Создаем все папки по очереди

---

## 🎭 Часть 2: Создание базового шаблона

### 🏗️ 2.1 Понимание наследования шаблонов
**Наследование** — это как в ООП: есть родительский класс (базовый шаблон) и дочерние классы (страницы), которые его расширяют.

### 📝 2.2 Создание base.html
**Создаем `templates/base.html`:**

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- ⭐ БЛОК TITLE -->
    <title>
        {% block title %}Шаблоны Django{% endblock %}
    </title>
    
    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- ⭐ БЛОК STYLES -->
    {% block styles %}
    <style>
        :root {
            --primary: #4e73df;
            --secondary: #858796;
            --success: #1cc88a;
            --light: #f8f9fc;
        }
        
        body {
            background: linear-gradient(135deg, #f8f9fc 0%, #e3e6f0 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        
        .demo-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            border: none;
            transition: all 0.3s ease;
        }
        
        .demo-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        }
        
        .code-block {
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            overflow-x: auto;
        }
        
        .nav-pills .nav-link.active {
            background: var(--primary) !important;
        }
    </style>
    {% endblock %}
</head>
<body>
    <!-- ⭐ БЛОК HEADER -->
    {% block header %}
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow">
        <div class="container">
            <a class="navbar-brand" href="/">
                🎨 <strong>Django Шаблонизация</strong>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == '/' %}active{% endif %}" href="/">
                            🏠 Главная
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/blocks/">
                            📦 Блоки
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/variables/">
                            🔤 Переменные
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/filters/">
                            🎛️ Фильтры
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/tags/">
                            🔄 Теги
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/inheritance/">
                            🧬 Наследование
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    {% endblock %}

    <!-- ⭐ БЛОК CONTENT -->
    <main class="container py-5">
        {% block content %}
        <!-- Здесь будет меняться содержимое страниц -->
        <div class="text-center">
            <h1 class="display-4 mb-4">🎯 Выберите тему для изучения</h1>
            <p class="lead">Используйте меню навигации для перехода к разделам</p>
        </div>
        {% endblock %}
    </main>

    <!-- ⭐ БЛОК FOOTER -->
    {% block footer %}
    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>📚 Учебный проект</h5>
                    <p>Изучение шаблонизации в Django</p>
                </div>
                <div class="col-md-6 text-end">
                    <p>Создано с ❤️ для студентов</p>
                    <p class="mb-0">© {% now "Y" %}</p>
                </div>
            </div>
        </div>
    </footer>
    {% endblock %}

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- ⭐ БЛОК SCRIPTS -->
    {% block scripts %}
    {% endblock %}
</body>
</html>
```

### 🎯 2.3 Разбор блоков в базовом шаблоне

**Список созданных блоков:**
1. `{% block title %}` — заголовок страницы (вкладка браузера)
2. `{% block styles %}` — дополнительные стили CSS
3. `{% block header %}` — шапка сайта
4. `{% block content %}` — **ГЛАВНЫЙ БЛОК** с содержимым
5. `{% block footer %}` — подвал сайта
6. `{% block scripts %}` — дополнительные JavaScript

**Правила работы с блоками:**
- Блоки определяются в родительском шаблоне
- Блоки могут иметь содержимое по умолчанию
- Дочерние шаблоны могут переопределять блоки
- Блоки можно оставить пустыми

---

## 🧠 Часть 3: Создание представлений для демонстрации

### 📝 3.1 Простые представления
**Создаем `demo/views.py`:**

```python
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
```

### 🛣️ 3.2 Настройка URL
**Создаем `demo/urls.py`:**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blocks/', views.blocks_demo, name='blocks'),
    path('variables/', views.variables_demo, name='variables'),
    path('filters/', views.filters_demo, name='filters'),
    path('tags/', views.tags_demo, name='tags'),
    path('inheritance/', views.inheritance_demo, name='inheritance'),
    path('includes/', views.includes_demo, name='includes'),
]
```

**Обновляем главный `templatedemo/urls.py`:**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('demo.urls')),  # Все URL из приложения demo
]
```

---

## 📦 Часть 4: Демонстрация блоков

### 🎯 4.1 Создание шаблона с блоками
**Создаем `demo/templates/demo/blocks.html`:**

```html
{% extends 'base.html' %}

<!-- ⭐ ПЕРЕОПРЕДЕЛЕНИЕ БЛОКА TITLE -->
{% block title %}{{ page_title }} - Django Шаблонизация{% endblock %}

<!-- ⭐ ДОБАВЛЕНИЕ СТИЛЕЙ К БЛОКУ STYLES -->
{% block styles %}
{{ block.super }}  <!-- ⬅️ СОХРАНЯЕМ РОДИТЕЛЬСКИЕ СТИЛИ -->
<style>
    .block-demo {
        border-left: 5px solid var(--primary);
        padding-left: 20px;
        margin: 30px 0;
    }
    
    .block-example {
        background: #e3f2fd;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
</style>
{% endblock %}

<!-- ⭐ ПОЛНОЕ ПЕРЕОПРЕДЕЛЕНИЕ HEADER -->
{% block header %}
<nav class="navbar navbar-expand-lg navbar-dark bg-success shadow">
    <div class="container">
        <span class="navbar-brand">
            📦 <strong>Демо: Блоки</strong>
        </span>
        <a href="/" class="btn btn-light btn-sm">← На главную</a>
    </div>
</nav>
{% endblock %}

<!-- ⭐ ГЛАВНОЕ СОДЕРЖИМОЕ -->
{% block content %}
<div class="row">
    <div class="col-lg-8">
        <h1 class="display-5 mb-4">{{ page_title }}</h1>
        
        <!-- Пример 1: Простое переопределение -->
        <div class="block-demo">
            <h3>1. Простое переопределение блока</h3>
            <div class="block-example">
                <h4>Родительский шаблон (base.html):</h4>
                <div class="code-block">
{% raw %}{% block title %}Шаблоны Django{% endblock %}{% endraw %}
                </div>
                
                <h4>Дочерний шаблон (blocks.html):</h4>
                <div class="code-block">
{% raw %}{% block title %}{{ page_title }} - Django Шаблонизация{% endblock %}{% endraw %}
                </div>
                
                <h4>Результат:</h4>
                <div class="alert alert-info">
                    Заголовок вкладки: "<strong>{{ page_title }} - Django Шаблонизация</strong>"
                </div>
            </div>
        </div>
        
        <!-- Пример 2: Добавление к родительскому -->
        <div class="block-demo">
            <h3>2. Добавление к содержимому родителя</h3>
            <div class="block-example">
                <h4>Код с {{ block.super }}:</h4>
                <div class="code-block">
{% raw %}{% block styles %}
{{ block.super }}  ← СОХРАНЯЕМ РОДИТЕЛЬСКИЕ СТИЛИ
<style>
    .my-extra-style { color: red; }
</style>
{% endblock %}{% endraw %}
                </div>
                <p><code>{{ block.super }}</code> вставляет содержимое блока из родительского шаблона</p>
            </div>
        </div>
        
        <!-- Пример 3: Пустой блок -->
        <div class="block-demo">
            <h3>3. Пустой блок</h3>
            <div class="block-example">
                <div class="code-block">
{% raw %}{% block scripts %}{% endblock %}{% endraw %}
                </div>
                <p>Блок остается пустым, если дочерний шаблон его не переопределяет</p>
            </div>
        </div>
    </div>
    
    <div class="col-lg-4">
        <!-- Боковая панель -->
        <div class="demo-card">
            <h4>📌 Ключевые моменты</h4>
            <ul class="list-unstyled">
                <li class="mb-2">✅ <strong>Блоки</strong> определяются в родительском шаблоне</li>
                <li class="mb-2">✅ <strong>Переопределение</strong> происходит в дочерних</li>
                <li class="mb-2">✅ <code>{{ block.super }}</code> для добавления к родителю</li>
                <li class="mb-2">✅ Блоки могут быть <strong>пустыми</strong></li>
                <li>✅ Можно создавать <strong>любое количество</strong> блоков</li>
            </ul>
            
            <hr>
            
            <h5>🕒 Время генерации:</h5>
            <p class="text-muted">{{ current_time|date:"H:i:s" }}</p>
            
            <h5>📊 Статистика:</h5>
            <div class="progress mb-2">
                <div class="progress-bar" style="width: 25%">Блоки</div>
                <div class="progress-bar bg-secondary" style="width: 75%">Остальное</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

<!-- ⭐ ПЕРЕОПРЕДЕЛЕНИЕ FOOTER -->
{% block footer %}
<div class="bg-primary text-white py-3">
    <div class="container text-center">
        <p class="mb-0">🎯 Эта страница демонстрирует работу блоков в Django</p>
        <small>Время: {{ current_time|date:"H:i:s" }}</small>
    </div>
</div>
{% endblock %}

<!-- ⭐ ДОБАВЛЕНИЕ SCRIPTS -->
{% block scripts %}
<script>
console.log("📦 Страница блоков загружена!");
document.addEventListener('DOMContentLoaded', function() {
    const blocks = document.querySelectorAll('.block-demo');
    blocks.forEach((block, index) => {
        block.addEventListener('click', function() {
            alert(`Вы кликнули на блок #${index + 1}`);
        });
    });
});
</script>
{% endblock %}
```

### 🎯 4.2 Что мы сделали с блоками:
1. **Полностью переопределили** `header` и `footer`
2. **Добавили стили** к существующим через `{{ block.super }}`
3. **Использовали** переменные внутри блоков
4. **Добавили JavaScript** в блок `scripts`

---

## 🔤 Часть 5: Демонстрация переменных

### 🎯 5.1 Создание шаблона с переменными
**Создаем `demo/templates/demo/variables.html`:**

```html
{% extends 'base.html' %}

{% block title %}Переменные - Django Шаблонизация{% endblock %}

{% block styles %}
{{ block.super }}
<style>
    .var-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid;
    }
    
    .string { border-left-color: #4e73df; }
    .number { border-left-color: #1cc88a; }
    .list { border-left-color: #f6c23e; }
    .dict { border-left-color: #e74a3b; }
    .bool { border-left-color: #6f42c1; }
    
    .code-inline {
        background: #f8f9fc;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        color: #d63384;
    }
    
    .result {
        background: #e7f3ff;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        font-family: monospace;
    }
</style>
{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <h1 class="display-5 mb-4">🔤 Работа с переменными в Django</h1>
        
        <!-- Строковая переменная -->
        <div class="var-card string">
            <h3>📝 Строка (String)</h3>
            <p><strong>Переменная:</strong> <code class="code-inline">string_var</code></p>
            <p><strong>Значение:</strong> <code>"{{ string_var }}"</code></p>
            <p><strong>Использование в шаблоне:</strong></p>
            <div class="code-block">
{{ string_var }}
            </div>
            <p><strong>Результат:</strong></p>
            <div class="result">{{ string_var }}</div>
        </div>
        
        <!-- Числовые переменные -->
        <div class="var-card number">
            <h3>🔢 Числа (Integer & Float)</h3>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Целое число:</strong></p>
                    <p><code class="code-inline">number_var</code> = {{ number_var }}</p>
                    <div class="code-block">
{{ number_var }} + 10 = {{ number_var|add:10 }}
                    </div>
                    <div class="result">{{ number_var }} + 10 = {{ number_var|add:10 }}</div>
                </div>
                <div class="col-md-6">
                    <p><strong>Дробное число:</strong></p>
                    <p><code class="code-inline">float_var</code> = {{ float_var }}</p>
                    <div class="code-block">
{{ float_var }} × 2 = {{ float_var|mul:2 }}
                    </div>
                    <div class="result">{{ float_var }} × 2 = {{ float_var|mul:2 }}</div>
                </div>
            </div>
        </div>
        
        <!-- Список -->
        <div class="var-card list">
            <h3>📋 Список (List)</h3>
            <p><strong>Переменная:</strong> <code class="code-inline">list_var</code></p>
            <p><strong>Значение:</strong> <code>["Python", "Django", "HTML", "CSS"]</code></p>
            
            <h5>Обращение по индексу:</h5>
            <div class="code-block">
{{ list_var.0 }}  ← Первый элемент<br>
{{ list_var.1 }}  ← Второй элемент<br>
{{ list_var|last }}  ← Последний элемент (фильтр)
            </div>
            <div class="result">
                {{ list_var.0 }}<br>
                {{ list_var.1 }}<br>
                {{ list_var|last }}
            </div>
            
            <h5 class="mt-3">Длина списка:</h5>
            <div class="code-block">
В списке {{ list_var|length }} элемента
            </div>
            <div class="result">В списке {{ list_var|length }} элемента</div>
        </div>
        
        <!-- Словарь -->
        <div class="var-card dict">
            <h3>🗂️ Словарь (Dictionary)</h3>
            <p><strong>Переменная:</strong> <code class="code-inline">dict_var</code></p>
            <p><strong>Значение:</strong> <code>{'name': 'Иван', 'age': 25, 'city': 'Москва'}</code></p>
            
            <h5>Обращение по ключу:</h5>
            <div class="code-block">
Имя: {{ dict_var.name }}<br>
Возраст: {{ dict_var.age }}<br>
Город: {{ dict_var.city }}
            </div>
            <div class="result">
                Имя: {{ dict_var.name }}<br>
                Возраст: {{ dict_var.age }}<br>
                Город: {{ dict_var.city }}
            </div>
            
            <h5 class="mt-3">Альтернативный синтаксис:</h5>
            <div class="code-block">
Имя: {{ dict_var.name }} = {{ dict_var.name }}<br>
Имя: {{ dict_var.name }} = {{ dict_var.name }}
            </div>
        </div>
        
        <!-- Булевы значения -->
        <div class="var-card bool">
            <h3>✅❌ Булевы значения (Boolean)</h3>
            <p><strong>Переменная:</strong> <code class="code-inline">bool_var</code></p>
            <p><strong>Значение:</strong> <code>{{ bool_var }}</code></p>
            
            <div class="code-block">
{% if bool_var %}
Переменная bool_var равна True
{% else %}
Переменная bool_var равна False
{% endif %}
            </div>
            <div class="result">
                {% if bool_var %}
                Переменная bool_var равна True
                {% else %}
                Переменная bool_var равна False
                {% endif %}
            </div>
        </div>
        
        <!-- None -->
        <div class="var-card">
            <h3>🚫 None (Пустое значение)</h3>
            <p><strong>Переменная:</strong> <code class="code-inline">none_var</code></p>
            <p><strong>Значение:</strong> <code>{{ none_var }}</code></p>
            
            <div class="code-block">
{% if none_var %}
Переменная не пустая
{% else %}
Переменная пустая (None)
{% endif %}
            </div>
            <div class="result">
                {% if none_var %}
                Переменная не пустая
                {% else %}
                Переменная пустая (None)
                {% endif %}
            </div>
        </div>
    </div>
    
    <div class="col-lg-4">
        <!-- Боковая панель -->
        <div class="demo-card">
            <h4>🎯 Основные типы переменных</h4>
            
            <h5 class="mt-4">📝 Строки</h5>
            <ul>
                <li>Текст в кавычках</li>
                <li><code>{{ "текст" }}</code></li>
            </ul>
            
            <h5>🔢 Числа</h5>
            <ul>
                <li>Целые: <code>42</code></li>
                <li>Дробные: <code>3.14</code></li>
            </ul>
            
            <h5>📋 Списки</h5>
            <ul>
                <li>По индексу: <code>list.0</code></li>
                <li>Длина: <code>list|length</code></li>
            </ul>
            
            <h5>🗂️ Словари</h5>
            <ul>
                <li>По ключу: <code>dict.key</code></li>
                <li>Или: <code>dict['key']</code></li>
            </ul>
            
            <h5>✅ Булевы</h5>
            <ul>
                <li><code>True</code> / <code>False</code></li>
                <li>Для условий <code>{% verbatim %}{% if %}{% endverbatim %}</code></li>
            </ul>
            
            <h5>🚫 None</h5>
            <ul>
                <li>Пустое значение</li>
                <li>Проверка: <code>{% verbatim %}{% if var %}{% endverbatim %}</code></li>
            </ul>
        </div>
        
        <div class="demo-card bg-light">
            <h5>💡 Совет</h5>
            <p>Все переменные передаются из view в шаблон через <strong>context</strong> словарь:</p>
            <div class="code-block">
def view(request):
    context = {
        'var1': 'значение',
        'var2': 123,
    }
    return render(request, 'template.html', context)
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 🎯 5.2 Ключевые моменты о переменных:
1. **Доступ через точку**: `object.attribute`
2. **Индексация списков**: `list.0`, `list.1`
3. **Ключи словарей**: `dict.key` или `dict['key']`
4. **Булевы значения** для условий
5. **None** — специальное пустое значение

---

## 🎛️ Часть 6: Демонстрация фильтров

### 🎯 6.1 Создание шаблона с фильтрами
**Создаем `demo/templates/demo/filters.html`:**

```html
{% extends 'base.html' %}

{% block title %}Фильтры - Django Шаблонизация{% endblock %}

{% block styles %}
{{ block.super }}
<style>
    .filter-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .filter-table th {
        background: #4e73df;
        color: white;
        padding: 12px;
        text-align: left;
    }
    
    .filter-table td {
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    
    .filter-table tr:hover {
        background: #f8f9fc;
    }
    
    .input-output {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 20px;
        margin: 20px 0;
    }
    
    .input-box, .output-box {
        padding: 15px;
        border-radius: 8px;
    }
    
    .input-box {
        background: #f8f9fc;
        border: 1px solid #e3e6f0;
    }
    
    .output-box {
        background: #e7f3ff;
        border: 1px solid #cfe2ff;
    }
</style>
{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <h1 class="display-5 mb-4">🎛️ Фильтры в Django Template Language</h1>
        
        <!-- Фильтры для строк -->
        <div class="demo-card">
            <h3>📝 Строковые фильтры</h3>
            
            <div class="input-output">
                <div class="input-box">
                    <h5>Исходная строка:</h5>
                    <code>"{{ long_text }}"</code>
                </div>
                <div class="output-box">
                    <h5>Фильтр <code>truncatechars:30</code>:</h5>
                    "{{ long_text|truncatechars:30 }}"
                </div>
            </div>
            
            <div class="input-output">
                <div class="input-box">
                    <h5>Исходная строка:</h5>
                    <code>"{{ sentence }}"</code>
                </div>
                <div class="output-box">
                    <h5>Фильтр <code>title</code>:</h5>
                    "{{ sentence|title }}"
                </div>
            </div>
            
            <div class="input-output">
                <div class="input-box">
                    <h5>Исходная строка:</h5>
                    <code>"{{ html_text }}"</code>
                </div>
                <div class="output-box">
                    <h5>Фильтр <code>safe</code>:</h5>
                    {{ html_text|safe }}
                    <p class="text-danger mt-2"><small>⚠️ Опасный HTML выполнится!</small></p>
                    
                    <h5 class="mt-3">Без фильтра:</h5>
                    {{ html_text }}
                    <p class="text-success"><small>✅ Безопасный вывод по умолчанию</small></p>
                </div>
            </div>
            
            <table class="filter-table mt-4">
                <thead>
                    <tr>
                        <th>Фильтр</th>
                        <th>Пример</th>
                        <th>Результат</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>upper</code></td>
                        <td><code>{{ string_var|upper }}</code></td>
                        <td>{{ string_var|upper }}</td>
                    </tr>
                    <tr>
                        <td><code>lower</code></td>
                        <td><code>{{ string_var|lower }}</code></td>
                        <td>{{ string_var|lower }}</td>
                    </tr>
                    <tr>
                        <td><code>capfirst</code></td>
                        <td><code>{{ "привет"|capfirst }}</code></td>
                        <td>{{ "привет"|capfirst }}</td>
                    </tr>
                    <tr>
                        <td><code>length</code></td>
                        <td><code>{{ string_var|length }}</code></td>
                        <td>{{ string_var|length }} символов</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Фильтры для чисел -->
        <div class="demo-card">
            <h3>🔢 Числовые фильтры</h3>
            
            <div class="input-output">
                <div class="input-box">
                    <h5>Исходное число:</h5>
                    <code>{{ price }}</code>
                </div>
                <div class="output-box">
                    <h5>Фильтр <code>floatformat:2</code>:</h5>
                    {{ price|floatformat:2 }} ₽
                </div>
            </div>
            
            <table class="filter-table mt-4">
                <thead>
                    <tr>
                        <th>Фильтр</th>
                        <th>Пример</th>
                        <th>Результат</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>add:10</code></td>
                        <td><code>{{ number_var|add:10 }}</code></td>
                        <td>{{ number_var|add:10 }}</td>
                    </tr>
                    <tr>
                        <td><code>mul:2</code></td>
                        <td><code>{{ number_var|mul:2 }}</code></td>
                        <td>{{ number_var|mul:2 }}</td>
                    </tr>
                    <tr>
                        <td><code>divisibleby:3</code></td>
                        <td><code>{{ number_var|divisibleby:3 }}</code></td>
                        <td>{{ number_var|divisibleby:3 }}</td>
                    </tr>
                    <tr>
                        <td><code>filesizeformat</code></td>
                        <td><code>1048576|filesizeformat</code></td>
                        <td>{{ 1048576|filesizeformat }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Фильтры для списков -->
        <div class="demo-card">
            <h3>📋 Фильтры для списков</h3>
            
            <div class="row">
                <div class="col-md-6">
                    <h5>Исходный список:</h5>
                    <code>{{ numbers }}</code>
                    
                    <h5 class="mt-3"><code>slice:":3"</code>:</h5>
                    {{ numbers|slice:":3" }}
                    
                    <h5 class="mt-3"><code>join:", "</code>:</h5>
                    {{ numbers|join:", " }}
                </div>
                <div class="col-md-6">
                    <h5><code>first</code>:</h5>
                    {{ numbers|first }}
                    
                    <h5 class="mt-3"><code>last</code>:</h5>
                    {{ numbers|last }}
                    
                    <h5 class="mt-3"><code>random</code>:</h5>
                    {{ numbers|random }}
                </div>
            </div>
        </div>
        
        <!-- Фильтры для дат -->
        <div class="demo-card">
            <h3>📅 Фильтры для дат</h3>
            
            <div class="input-output">
                <div class="input-box">
                    <h5>Исходная дата:</h5>
                    <code>{{ current_date }}</code>
                </div>
                <div class="output-box">
                    <h5>Разные форматы:</h5>
                    <code>date:"d.m.Y"</code>: {{ current_date|date:"d.m.Y" }}<br>
                    <code>date:"H:i:s"</code>: {{ current_date|date:"H:i:s" }}<br>
                    <code>date:"j F Y"</code>: {{ current_date|date:"j F Y" }}<br>
                    <code>timesince</code>: {{ current_date|timesince }}
                </div>
            </div>
        </div>
        
        <!-- Цепочки фильтров -->
        <div class="demo-card">
            <h3>⛓️ Цепочки фильтров</h3>
            <p>Фильтры можно объединять в цепочки (выполняются слева направо):</p>
            
            <div class="code-block">
{{ string_var|upper|slice:":10" }}  ← Сначала верхний регистр, затем обрезка
            </div>
            <div class="result">
                {{ string_var|upper|slice:":10" }}
            </div>
            
            <div class="code-block">
{{ price|floatformat:2|add:"0" }} ₽  ← Сначала форматирование, затем сложение
            </div>
            <div class="result">
                {{ price|floatformat:2|add:"0" }} ₽
            </div>
        </div>
    </div>
    
    <div class="col-lg-4">
        <div class="demo-card">
            <h4>🎛️ Популярные фильтры</h4>
            
            <h5 class="mt-3">📝 Для строк:</h5>
            <ul>
                <li><code>lower</code> — нижний регистр</li>
                <li><code>upper</code> — верхний регистр</li>
                <li><code>title</code> — Заглавные Буквы</li>
                <li><code>truncatechars:N</code> — обрезать</li>
                <li><code>length</code> — длина</li>
            </ul>
            
            <h5>🔢 Для чисел:</h5>
            <ul>
                <li><code>add:N</code> — прибавить</li>
                <li><code>floatformat:N</code> — N знаков</li>
                <li><code>filesizeformat</code> — размер файла</li>
            </ul>
            
            <h5>📋 Для списков:</h5>
            <ul>
                <li><code>first</code> / <code>last</code></li>
                <li><code>join:"sep"</code> — объединить</li>
                <li><code>slice</code> — срез</li>
                <li><code>random</code> — случайный</li>
            </ul>
            
            <h5>📅 Для дат:</h5>
            <ul>
                <li><code>date:"формат"</code></li>
                <li><code>timesince</code> — сколько прошло</li>
                <li><code>timeuntil</code> — сколько осталось</li>
            </ul>
            
            <h5>🛡️ Безопасность:</h5>
            <ul>
                <li><code>safe</code> — вывести HTML</li>
                <li><code>escape</code> — экранировать</li>
                <li><code>force_escape</code> — принудительно</li>
            </ul>
        </div>
        
        <div class="demo-card bg-warning bg-opacity-10">
            <h5>⚠️ Важно!</h5>
            <p>Фильтр <code>safe</code> может быть опасен! Он отключает автоматическое экранирование HTML.</p>
            <p>Используйте только с доверенными данными!</p>
        </div>
    </div>
</div>
{% endblock %}
```

### 🎯 6.2 Основные фильтры Django:
1. **Строковые**: `upper`, `lower`, `title`, `truncatechars`
2. **Числовые**: `add`, `floatformat`, `filesizeformat`
3. **Для списков**: `first`, `last`, `join`, `slice`
4. **Для дат**: `date`, `timesince`, `timeuntil`
5. **Безопасность**: `safe`, `escape`

---

## 🔄 Часть 7: Демонстрация тегов

### 🎯 7.1 Создание шаблона с тегами
**Создаем `demo/templates/demo/tags.html`:**

```html
{% extends 'base.html' %}

{% block title %}Теги - Django Шаблонизация{% endblock %}

{% block styles %}
{{ block.super }}
<style>
    .tag-example {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #e3e6f0;
    }
    
    .tag-code {
        background: #f8f9fc;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        font-family: monospace;
    }
    
    .tag-result {
        background: #e7f3ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4e73df;
    }
    
    .loop-item {
        padding: 10px;
        margin: 5px 0;
        background: #f8f9fc;
        border-radius: 5px;
    }
</style>
{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <h1 class="display-5 mb-4">🔄 Теги в Django Template Language</h1>
        
        <!-- Тег for -->
        <div class="tag-example">
            <h3>🔄 Тег <code>{% verbatim %}{% for %}{% endverbatim %}</code></h3>
            <p>Используется для перебора списков, словарей и других итерируемых объектов.</p>
            
            <div class="tag-code">
{% verbatim %}{% for item in items %}
    {{ forloop.counter }}. {{ item }}
{% endfor %}{% endverbatim %}
            </div>
            
            <div class="tag-result">
                {% for item in items %}
                <div class="loop-item">
                    {{ forloop.counter }}. {{ item }}
                    <small class="text-muted">
                        (первый: {{ forloop.first }}, 
                        последний: {{ forloop.last }},
                        индекс: {{ forloop.counter0 }})
                    </small>
                </div>
                {% endfor %}
            </div>
            
            <h5 class="mt-3">Переменные цикла <code>forloop</code>:</h5>
            <ul>
                <li><code>forloop.counter</code> — номер итерации (1, 2, 3...)</li>
                <li><code>forloop.counter0</code> — номер итерации (0, 1, 2...)</li>
                <li><code>forloop.revcounter</code> — обратный счетчик</li>
                <li><code>forloop.first</code> — первая итерация?</li>
                <li><code>forloop.last</code> — последняя итерация?</li>
            </ul>
        </div>
        
        <!-- Тег if -->
        <div class="tag-example">
            <h3>✅ Тег <code>{% verbatim %}{% if %}{% endverbatim %}</code></h3>
            <p>Условное выполнение блока кода.</p>
            
            <div class="tag-code">
{% verbatim %}{% if user.is_admin %}
    👑 Администратор
{% elif user.name %}
    👤 {{ user.name }}
{% else %}
    🎭 Гость
{% endif %}{% endverbatim %}
            </div>
            
            <div class="tag-result">
                {% if user.is_admin %}
                👑 Администратор
                {% elif user.name %}
                👤 {{ user.name }}
                {% else %}
                🎭 Гость
                {% endif %}
            </div>
            
            <h5 class="mt-3">Операторы в условиях:</h5>
            <ul>
                <li><code>==</code>, <code>!=</code> — равно/не равно</li>
                <li><code>&lt;</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&gt;=</code></li>
                <li><code>in</code> — вхождение в список</li>
                <li><code>not in</code> — не входит в список</li>
                <li><code>and</code>, <code>or</code> — логические</li>
                <li><code>not</code> — отрицание</li>
            </ul>
        </div>
        
        <!-- Тег with -->
        <div class="tag-example">
            <h3>📝 Тег <code>{% verbatim %}{% with %}{% endverbatim %}</code></h3>
            <p>Создает локальную переменную с псевдонимом.</p>
            
            <div class="tag-code">
{% verbatim %}{% with total=items|length %}
    Всего элементов: {{ total }}
{% endwith %}{% endverbatim %}
            </div>
            
            <div class="tag-result">
                {% with total=items|length %}
                Всего элементов: {{ total }}
                {% endwith %}
            </div>
        </div>
        
        <!-- Тег empty -->
        <div class="tag-example">
            <h3>📭 Тег <code>{% verbatim %}{% empty %}{% endverbatim %}</code></h3>
            <p>Выполняется, если цикл for не имеет элементов.</p>
            
            <div class="tag-code">
{% verbatim %}{% for item in empty_list %}
    {{ item }}
{% empty %}
    🎒 Список пуст!
{% endfor %}{% endverbatim %}
            </div>
            
            <div class="tag-result">
                {% for item in empty_list %}
                {{ item }}
                {% empty %}
                🎒 Список пуст!
                {% endfor %}
            </div>
        </div>
        
        <!-- Тег ifchanged -->
        <div class="tag-example">
            <h3>🔄 Тег <code>{% verbatim %}{% ifchanged %}{% endverbatim %}</code></h3>
            <p>Выполняет блок только если значение изменилось с предыдущей итерации.</p>
            
            <div class="tag-code">
{% verbatim %}{% for post in posts %}
{% ifchanged post.published %}
    {% if post.published %}
        📢 Опубликованные:
    {% else %}
        📝 Черновики:
    {% endif %}
{% endifchanged %}
    - {{ post.title }}
{% endfor %}{% endverbatim %}
            </div>
            
            <div class="tag-result">
                {% for post in posts %}
                {% ifchanged post.published %}
                    {% if post.published %}
                    📢 Опубликованные:
                    {% else %}
                    📝 Черновики:
                    {% endif %}
                {% endifchanged %}
                <div class="loop-item">- {{ post.title }}</div>
                {% endfor %}
            </div>
        </div>
        
        <!-- Комментарии -->
        <div class="tag-example">
            <h3>💭 Комментарии</h3>
            <p>Комментарии не отображаются в итоговом HTML.</p>
            
            <div class="tag-code">
{% verbatim %}{# Это однострочный комментарий #}
{% comment "Пояснение" %}
    Это многострочный комментарий.
    Он может занимать несколько строк.
    Ничто внутри не будет выполнено.
{% endcomment %}{% endverbatim %}
            </div>
        </div>
        
        <!-- Цикл по словарю -->
        <div class="tag-example">
            <h3>🗂️ Цикл по словарю</h3>
            
            <div class="tag-code">
{% verbatim %}{% for key, value in dict_var.items %}
    {{ key }}: {{ value }}
{% endfor %}{% endverbatim %}
            </div>
            
            <div class="tag-result">
                {% for key, value in dict_var.items %}
                <div class="loop-item">
                    <strong>{{ key }}</strong>: {{ value }}
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="col-lg-4">
        <div class="demo-card">
            <h4>🔄 Основные теги</h4>
            
            <h5 class="mt-3">Управление потоком:</h5>
            <ul>
                <li><code>{% verbatim %}{% for %}{% endverbatim %}</code> — цикл</li>
                <li><code>{% verbatim %}{% if %}{% endverbatim %}</code> — условие</li>
                <li><code>{% verbatim %}{% elif %}{% endverbatim %}</code> — иначе если</li>
                <li><code>{% verbatim %}{% else %}{% endverbatim %}</code> — иначе</li>
            </ul>
            
            <h5>Переменные:</h5>
            <ul>
                <li><code>{% verbatim %}{% with %}{% endverbatim %}</code> — локальная переменная</li>
                <li><code>{% verbatim %}{% widthratio %}{% endverbatim %}</code> — пропорция</li>
            </ul>
            
            <h5>Циклы:</h5>
            <ul>
                <li><code>{% verbatim %}{% empty %}{% endverbatim %}</code> — если пусто</li>
                <li><code>{% verbatim %}{% ifchanged %}{% endverbatim %}</code> — если изменилось</li>
            </ul>
            
            <h5>Наследование:</h5>
            <ul>
                <li><code>{% verbatim %}{% block %}{% endverbatim %}</code> — определение блока</li>
                <li><code>{% verbatim %}{% extends %}{% endverbatim %}</code> — наследование</li>
                <li><code>{{ block.super }}</code> — родительское содержимое</li>
            </ul>
            
            <h5>Включения:</h5>
            <ul>
                <li><code>{% verbatim %}{% include %}{% endverbatim %}</code> — включение шаблона</li>
            </ul>
            
            <h5>Комментарии:</h5>
            <ul>
                <li><code>{# ... #}</code> — однострочный</li>
                <li><code>{% verbatim %}{% comment %}{% endverbatim %}</code> — многострочный</li>
            </ul>
        </div>
        
        <div class="demo-card bg-info bg-opacity-10">
            <h5>💡 Пример сложного условия:</h5>
            <div class="tag-code">
{% verbatim %}{% if score >= 90 and user.is_admin or score >= 80 %}
    Высокий результат!
{% endif %}{% endverbatim %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 🎯 7.2 Основные теги Django:
1. **Управление потоком**: `for`, `if`, `elif`, `else`
2. **Переменные**: `with`, `widthratio`
3. **Циклы**: `empty`, `ifchanged`
4. **Наследование**: `block`, `extends`, `block.super`
5. **Включения**: `include`
6. **Комментарии**: `{# #}`, `{% comment %}`

---

## 🧩 Часть 8: Включения (includes) и пользовательские теги

### 🎯 8.1 Создание включаемых шаблонов
**Создаем `demo/templates/demo/includes/` и файлы:**

**`demo/templates/demo/includes/alert.html`:**
```html
<div class="alert alert-{{ type|default:'info' }} alert-dismissible fade show" role="alert">
    {% if icon %}
    <i class="{{ icon }} me-2"></i>
    {% endif %}
    
    <strong>{{ title|default:'Внимание!' }}</strong> {{ message }}
    
    {% if dismissible %}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    {% endif %}
</div>
```

**`demo/templates/demo/includes/card.html`:**
```html
<div class="card {{ class }}">
    {% if header %}
    <div class="card-header">
        {{ header }}
    </div>
    {% endif %}
    
    <div class="card-body">
        {% if title %}
        <h5 class="card-title">{{ title }}</h5>
        {% endif %}
        
        {% if text %}
        <p class="card-text">{{ text }}</p>
        {% endif %}
        
        {% if content %}
        {{ content }}
        {% endif %}
    </div>
    
    {% if footer %}
    <div class="card-footer">
        {{ footer }}
    </div>
    {% endif %}
</div>
```

### 🎯 8.2 Шаблон с включениями
**Создаем `demo/templates/demo/includes.html`:**

```html
{% extends 'base.html' %}

{% block title %}Включения - Django Шаблонизация{% endblock %}

{% block content %}
<h1 class="display-5 mb-4">🧩 Включение шаблонов</h1>

<div class="row">
    <div class="col-lg-8">
        <div class="demo-card">
            <h3>📦 Тег <code>{% verbatim %}{% include %}{% endverbatim %}</code></h3>
            <p>Позволяет включать один шаблон в другой.</p>
            
            <h5 class="mt-4">Простое включение:</h5>
            <div class="tag-code">
{% verbatim %}{% include "demo/includes/alert.html" %}{% endverbatim %}
            </div>
            {% include "demo/includes/alert.html" %}
            
            <h5 class="mt-4">С передачей переменных:</h5>
            <div class="tag-code">
{% verbatim %}{% include "demo/includes/alert.html" with 
    type="success" 
    icon="bi bi-check-circle"
    title="Успех!" 
    message="Операция выполнена успешно."
    dismissible=True
%}{% endverbatim %}
            </div>
            {% include "demo/includes/alert.html" with 
                type="success" 
                icon="bi bi-check-circle"
                title="Успех!" 
                message="Операция выполнена успешно."
                dismissible=True
            %}
            
            <h5 class="mt-4">Карточка с контентом:</h5>
            {% include "demo/includes/card.html" with 
                header="Пример карточки"
                title="Заголовок карточки"
                text="Это содержимое карточки, переданное через переменные."
                footer="Подвал карточки"
                class="border-primary"
            %}
        </div>
    </div>
    
    <div class="col-lg-4">
        <div class="demo-card">
            <h4>🎯 Преимущества includes</h4>
            <ul>
                <li>📁 <strong>Повторное использование</strong> кода</li>
                <li>🎨 <strong>Единообразие</strong> элементов</li>
                <li>🔧 <strong>Легкое обновление</strong> в одном месте</li>
                <li>🧩 <strong>Модульность</strong> кода</li>
                <li>⚡ <strong>Кэширование</strong> включений</li>
            </ul>
            
            <hr>
            
            <h5>💡 Когда использовать?</h5>
            <ul>
                <li>Навигационные меню</li>
                <li>Футеры и хедеры</li>
                <li>Карточки товаров</li>
                <li>Формы</li>
                <li>Сообщения</li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}
```

### 🎯 8.3 Создание пользовательских фильтров и тегов
**Создаем структуру:**
```
demo/
├── templatetags/           # ⬅️ ОБЯЗАТЕЛЬНОЕ ИМЯ
│   ├── __init__.py
│   ├── demo_tags.py       # Пользовательские теги
│   └── demo_filters.py    # Пользовательские фильтры
```

**`demo/templatetags/demo_filters.py`:**
```python
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Умножает значение на аргумент"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def split_lines(value):
    """Разбивает текст на строки и оборачивает в <p>"""
    if not value:
        return ""
    lines = value.split('\n')
    return ''.join(f'<p>{line}</p>' for line in lines if line.strip())

@register.filter
def format_phone(value):
    """Форматирует телефонный номер"""
    if not value:
        return ""
    phone = str(value).replace(' ', '').replace('-', '')
    if len(phone) == 11:
        return f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    return value
```

**`demo/templatetags/demo_tags.py`:**
```python
from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def current_time(format_string="%H:%M:%S"):
    """Возвращает текущее время в указанном формате"""
    return datetime.now().strftime(format_string)

@register.simple_tag
def greeting(name="Гость"):
    """Возвращает приветствие"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        time_greeting = "Доброе утро"
    elif 12 <= hour < 18:
        time_greeting = "Добрый день"
    elif 18 <= hour < 23:
        time_greeting = "Добрый вечер"
    else:
        time_greeting = "Доброй ночи"
    
    return f"{time_greeting}, {name}!"

@register.inclusion_tag('demo/includes/tag_demo.html')
def show_user_card(user):
    """Отображает карточку пользователя"""
    return {'user': user}
```

**Создаем `demo/templates/demo/includes/tag_demo.html`:**
```html
<div class="card">
    <div class="card-body">
        <h5 class="card-title">{{ user.name }}</h5>
        <p class="card-text">
            {% if user.is_admin %}
            <span class="badge bg-danger">Админ</span>
            {% else %}
            <span class="badge bg-secondary">Пользователь</span>
            {% endif %}
        </p>
    </div>
</div>
```

---

## 🚀 Часть 9: Запуск и тестирование

### 🔄 9.1 Применяем миграции
```bash
python manage.py migrate
```

### 👑 9.2 Создаем суперпользователя
```bash
python manage.py createsuperuser
# Логин: admin
# Пароль: admin123
```

### 🚦 9.3 Запускаем сервер
```bash
python manage.py runserver
```

### 🌐 9.4 Тестируем все страницы:
1. **Главная**: http://127.0.0.1:8000/
2. **Блоки**: http://127.0.0.1:8000/blocks/
3. **Переменные**: http://127.0.0.1:8000/variables/
4. **Фильтры**: http://127.0.0.1:8000/filters/
5. **Теги**: http://127.0.0.1:8000/tags/
6. **Включения**: http://127.0.0.1:8000/includes/

---

## 📚 Часть 10: Шпаргалка по шаблонизации Django

### 🎯 Основные конструкции:

| Конструкция | Синтаксис | Назначение |
|------------|-----------|------------|
| **Переменная** | `{{ variable }}` | Вывод значения |
| **Фильтр** | `{{ var|filter }}` | Преобразование |
| **Тег** | `{% tag %}` | Логика шаблона |
| **Комментарий** | `{# текст #}` | Комментарий |
| **Блок** | `{% block name %}` | Определение блока |
| **Наследование** | `{% extends %}` | Наследование |
| **Включение** | `{% include %}` | Включение шаблона |

### 📦 Блоки:

```html
<!-- Родительский шаблон -->
{% block content %}
  Содержимое по умолчанию
{% endblock %}

<!-- Дочерний шаблон -->
{% block content %}
  {{ block.super }}  <!-- Родительское содержимое -->
  Новое содержимое
{% endblock %}
```

### 🔤 Переменные:

```html
{{ object.attribute }}      <!-- Атрибут объекта -->
{{ list.0 }}               <!-- Элемент списка -->
{{ dict.key }}             <!-- Значение словаря -->
{{ dict.key }}             <!-- Альтернатива -->
```

### 🎛️ Популярные фильтры:

```html
{{ text|upper }}           <!-- Верхний регистр -->
{{ text|truncatechars:50 }}<!-- Обрезать текст -->
{{ number|floatformat:2 }} <!-- Два знака после запятой -->
{{ list|join:", " }}       <!-- Объединить список -->
{{ date|date:"d.m.Y" }}    <!-- Формат даты -->
{{ html|safe }}            <!-- Безопасный HTML -->
```

### 🔄 Основные теги:

```html
{% for item in items %}    <!-- Цикл -->
{% if condition %}         <!-- Условие -->
{% elif condition %}       <!-- Иначе если -->
{% else %}                 <!-- Иначе -->
{% empty %}                <!-- Если пусто -->
{% with var=value %}       <!-- Локальная переменная -->
{% include "path" %}       <!-- Включение -->
{% extends "base.html" %}  <!-- Наследование -->
{% block name %}           <!-- Определение блока -->
```

### 🧩 Включения:

```html
<!-- Простое включение -->
{% include "template.html" %}

<!-- С переменными -->
{% include "template.html" with var1=value1 var2=value2 %}

<!-- С контекстом -->
{% include "template.html" only %}
```

---

## 🎓 Итог: Что мы изучили?

### ✅ Основные концепции:
1. **Наследование шаблонов** — DRY принцип в действии
2. **Блоки и их переопределение** — гибкость шаблонов
3. **Переменные и их типы** — работа с данными
4. **Фильтры** — преобразование данных на лету
5. **Теги** — логика в шаблонах
6. **Включения** — модульность и повторное использование
7. **Пользовательские теги/фильтры** — расширение возможностей

### 🚀 Что дальше?
1. **Формы Django** — обработка пользовательского ввода
2. **Классовые представления** — более мощные views
3. **Кеширование шаблонов** — оптимизация производительности
4. **Международзация** — поддержка нескольких языков
5. **Статические файлы** — управление CSS, JS, изображениями

### 💡 Советы для начинающих:
1. **Всегда используйте наследование** — это экономит время
2. **Разделяйте логику и представление** — бизнес-логика в views, отображение в шаблонах
3. **Используйте фильтры** для простых преобразований
4. **Создавайте включаемые шаблоны** для повторяющихся элементов
5. **Не бойтесь создавать** свои теги и фильтры

---

## 🎉 Поздравляю! Вы освоили шаблонизацию Django!

Теперь вы можете создавать:
- 🏗️ **Сложные макеты** с наследованием
- 🔄 **Динамические страницы** с переменными
- 🎨 **Красивый интерфейс** с фильтрами
- 🧩 **Модульные компоненты** с включениями
- ⚡ **Эффективные шаблоны** с пользовательскими тегами

**Помните:** Хороший шаблон — это как хороший рецепт: понятный, модульный и легко изменяемый! 🚀
