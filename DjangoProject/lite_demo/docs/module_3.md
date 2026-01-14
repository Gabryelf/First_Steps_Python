# Модуль 3: Шаблонизация и расширение проекта

В этом модуле мы углубимся в систему шаблонов Django, добавим наследование шаблонов, статические файлы и расширим функционал нашего блога.

---

## Шаг 1: Создание базового шаблона (layout)

**Комментарий:** Наследование шаблонов позволяет создать общую структуру для всех страниц сайта. Это упрощает поддержку и изменение дизайна.

**Создадим базовый шаблон:**
```bash
mkdir -p main/templates/base
```

**Файл: main/templates/base/layout.html**
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Мой Django Блог{% endblock %}</title>
    
    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Собственные стили -->
    {% load static %}
    <link rel="stylesheet" href="{% static 'main/css/style.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Навигация -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Django Blog</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}">Главная</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'about' %}">О сайте</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/admin/" target="_blank">Админка</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Основной контент -->
    <main class="container">
        {% if messages %}
        <div class="messages">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}
        <!-- Содержимое будет здесь -->
        {% endblock %}
    </main>

    <!-- Футер -->
    <footer class="mt-5 py-4 bg-light border-top">
        <div class="container text-center">
            <p class="mb-0">&copy; {% now "Y" %} Мой Django Блог. Все права защищены.</p>
        </div>
    </footer>

    <!-- Скрипты -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'main/js/main.js' %}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## Шаг 2: Настройка статических файлов

**Комментарий:** Статические файлы (CSS, JavaScript, изображения) хранятся отдельно от кода. Django собирает их в одном месте при развертывании.

**Создадим структуру для статических файлов:**
```bash
mkdir -p main/static/main/css
mkdir -p main/static/main/js
mkdir -p main/static/main/images
```

**Файл: main/static/main/css/style.css**
```css
/* Основные стили */
body {
    background-color: #f8f9fa;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
}

/* Стили для карточек статей */
.article-card {
    transition: transform 0.3s ease;
    border: none;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.article-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.article-meta {
    color: #6c757d;
    font-size: 0.9em;
}

/* Стили для форм */
.form-control:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Стили для футера */
footer {
    margin-top: auto;
}
```

**Файл: main/static/main/js/main.js**
```javascript
// Основной JavaScript файл
document.addEventListener('DOMContentLoaded', function() {
    // Автоматическое скрытие alert через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить эту статью?')) {
                e.preventDefault();
            }
        });
    });
});
```

---

## Шаг 3: Обновляем главный шаблон

**Комментарий:** Теперь перепишем наш home.html, чтобы он наследовался от базового шаблона.

**Файл: main/templates/main/home.html**
```html
{% extends 'base/layout.html' %}
{% load static %}

{% block title %}Главная страница - Django Blog{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card mb-4">
            <div class="card-header bg-success text-white">
                <h2 class="h5 mb-0">Добавить новую статью</h2>
            </div>
            <div class="card-body">
                <form method="post" class="needs-validation" novalidate>
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label for="{{ form.title.id_for_label }}" class="form-label">
                            <strong>Заголовок:</strong>
                        </label>
                        {{ form.title }}
                        {% if form.title.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.title.errors }}
                            </div>
                        {% endif %}
                    </div>

                    <div class="mb-3">
                        <label for="{{ form.content.id_for_label }}" class="form-label">
                            <strong>Содержание:</strong>
                        </label>
                        {{ form.content }}
                        {% if form.content.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.content.errors }}
                            </div>
                        {% endif %}
                    </div>

                    <div class="mb-3 form-check">
                        {{ form.is_published }}
                        <label for="{{ form.is_published.id_for_label }}" class="form-check-label">
                            Опубликовать сразу
                        </label>
                    </div>

                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-save"></i> Сохранить статью
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Список статей -->
        <h3 class="mb-4">Последние статьи ({{ articles|length }})</h3>
        
        {% if articles %}
            {% for article in articles %}
            <div class="article-card card mb-4">
                <div class="card-body">
                    <h4 class="card-title">{{ article.title }}</h4>
                    
                    <div class="article-meta mb-3">
                        <i class="far fa-calendar"></i> {{ article.created_at|date:"d.m.Y H:i" }}
                        {% if not article.is_published %}
                            <span class="badge bg-warning text-dark ms-2">Черновик</span>
                        {% endif %}
                    </div>
                    
                    <p class="card-text">
                        {{ article.content|truncatewords:50 }}
                    </p>
                    
                    <div class="d-flex justify-content-between align-items-center">
                        <a href="{% url 'article_detail' article.id %}" class="btn btn-outline-primary btn-sm">
                            Читать далее
                        </a>
                        <div>
                            <a href="{% url 'article_edit' article.id %}" class="btn btn-outline-warning btn-sm">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="{% url 'article_delete' article.id %}" class="btn btn-outline-danger btn-sm btn-delete">
                                <i class="fas fa-trash"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="alert alert-info">
                Статей пока нет. Будьте первым, кто добавит статью!
            </div>
        {% endif %}
    </div>

    <!-- Боковая панель -->
    <div class="col-lg-4">
        <div class="card mb-4">
            <div class="card-header bg-info text-white">
                <h3 class="h5 mb-0">О сайте</h3>
            </div>
            <div class="card-body">
                <p>Это простой блог, созданный на Django. Здесь вы можете:</p>
                <ul>
                    <li>Добавлять статьи</li>
                    <li>Редактировать их</li>
                    <li>Управлять публикацией</li>
                </ul>
                <a href="{% url 'about' %}" class="btn btn-info">Подробнее</a>
            </div>
        </div>

        <div class="card">
            <div class="card-header bg-secondary text-white">
                <h3 class="h5 mb-0">Статистика</h3>
            </div>
            <div class="card-body">
                <p>Всего статей: <strong>{{ articles|length }}</strong></p>
                <p>Опубликовано: <strong>{{ published_count }}</strong></p>
                <p>Черновиков: <strong>{{ draft_count }}</strong></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_css %}
<!-- Font Awesome для иконок -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
{% endblock %}
```

---

## Шаг 4: Добавляем новые представления

**Комментарий:** Расширим функционал: добавим страницу "О сайте", детальный просмотр статей, редактирование и удаление.

**Файл: main/views.py (дополняем)**
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import ArticleForm
from .models import Article

def home(request):
    articles = Article.objects.all().order_by('-created_at')
    
    # Статистика
    published_count = Article.objects.filter(is_published=True).count()
    draft_count = Article.objects.filter(is_published=False).count()
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно добавлена!')
            return redirect('home')
    else:
        form = ArticleForm()
    
    return render(request, 'main/home.html', {
        'articles': articles,
        'form': form,
        'published_count': published_count,
        'draft_count': draft_count
    })

def about(request):
    """Страница 'О сайте'"""
    return render(request, 'main/about.html')

def article_detail(request, article_id):
    """Детальная страница статьи"""
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'main/article_detail.html', {'article': article})

def article_edit(request, article_id):
    """Редактирование статьи"""
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно обновлена!')
            return redirect('home')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'main/article_edit.html', {
        'form': form,
        'article': article
    })

def article_delete(request, article_id):
    """Удаление статьи"""
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья успешно удалена!')
        return redirect('home')
    
    return render(request, 'main/article_confirm_delete.html', {'article': article})
```

---

## Шаг 5: Создаем дополнительные шаблоны

**Файл: main/templates/main/about.html**
```html
{% extends 'base/layout.html' %}

{% block title %}О сайте - Django Blog{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h1 class="h3 mb-0">О нашем сайте</h1>
            </div>
            <div class="card-body">
                <p class="lead">Добро пожаловать в наш блог на Django!</p>
                <p>Это учебный проект, созданный для демонстрации возможностей Django.</p>
                
                <h4 class="mt-4">Что мы использовали:</h4>
                <ul>
                    <li>Django 4.x для бэкенда</li>
                    <li>Bootstrap 5 для фронтенда</li>
                    <li>SQLite для базы данных</li>
                    <li>Шаблоны Django для отображения</li>
                </ul>
                
                <h4 class="mt-4">Функционал:</h4>
                <div class="row">
                    <div class="col-md-6">
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5>CRUD операции</h5>
                                <p>Создание, чтение, обновление и удаление статей</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5>Админка</h5>
                                <p>Встроенная административная панель Django</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <a href="{% url 'home' %}" class="btn btn-primary mt-3">
                    <i class="fas fa-arrow-left"></i> Вернуться на главную
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Файл: main/templates/main/article_detail.html**
```html
{% extends 'base/layout.html' %}

{% block title %}{{ article.title }} - Django Blog{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-10">
        <article class="card">
            <div class="card-header bg-light">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb mb-0">
                        <li class="breadcrumb-item"><a href="{% url 'home' %}">Главная</a></li>
                        <li class="breadcrumb-item active">{{ article.title|truncatechars:30 }}</li>
                    </ol>
                </nav>
            </div>
            <div class="card-body">
                <h1 class="card-title">{{ article.title }}</h1>
                
                <div class="text-muted mb-4">
                    <small>
                        <i class="far fa-calendar"></i> Опубликовано: {{ article.created_at|date:"d.m.Y в H:i" }}
                        {% if not article.is_published %}
                            <span class="badge bg-warning text-dark ms-2">Черновик</span>
                        {% endif %}
                    </small>
                </div>
                
                <div class="article-content">
                    {{ article.content|linebreaks }}
                </div>
            </div>
            <div class="card-footer bg-light">
                <div class="d-flex justify-content-between">
                    <a href="{% url 'home' %}" class="btn btn-outline-secondary">
                        <i class="fas fa-arrow-left"></i> Назад к списку
                    </a>
                    <div>
                        <a href="{% url 'article_edit' article.id %}" class="btn btn-warning">
                            <i class="fas fa-edit"></i> Редактировать
                        </a>
                    </div>
                </div>
            </div>
        </article>
    </div>
</div>
{% endblock %}
```

---

## Шаг 6: Обновляем URL-маршруты

**Файл: main/urls.py**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:article_id>/delete/', views.article_delete, name='article_delete'),
]
```

---

## Шаг 7: Настройка статических файлов в settings.py

**Файл: mysite/settings.py (добавляем в конец)**
```python
# Статические файлы (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Папка, куда collectstatic будет собирать статические файлы для продакшена
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Дополнительные папки со статическими файлами
STATICFILES_DIRS = [
    BASE_DIR / 'main' / 'static',
]

# Медиа файлы (загруженные пользователями)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## Шаг 8: Запуск и проверка

```bash
# Применяем изменения в базе данных
python manage.py makemigrations
python manage.py migrate

# Собираем статические файлы
python manage.py collectstatic

# Создаем суперпользователя (если еще нет)
python manage.py createsuperuser

# Запускаем сервер
python manage.py runserver
```

**Что проверить:**

1. **Наследование шаблонов** - все страницы имеют одинаковый header и footer
2. **Статические файлы** - CSS и JavaScript подключаются корректно
3. **Навигация** - меню работает на всех страницах
4. **Новые страницы** - /about/, /article/1/, /article/1/edit/
5. **Сообщения** - всплывающие уведомления после действий
6. **Адаптивность** - сайт корректно отображается на мобильных устройствах

---

## Итог третьего модуля:

### Что мы добавили:
1. **Базовый шаблон** - система наследования для единообразия
2. **Статические файлы** - CSS, JavaScript, структура папок
3. **Навигацию** - единое меню для всего сайта
4. **Систему сообщений** - уведомления пользователю
5. **Дополнительные страницы** - "О сайте", детальный просмотр
6. **CRUD операции** - полный цикл работы со статьями
7. **Адаптивный дизайн** - Bootstrap 5 для мобильных устройств
8. **Иконки** - Font Awesome для визуального улучшения

### Архитектура проекта теперь:
```
mysite/
├── main/
│   ├── static/
│   │   └── main/
│   │       ├── css/
│   │       │   └── style.css
│   │       ├── js/
│   │       │   └── main.js
│   │       └── images/
│   ├── templates/
│   │   ├── base/
│   │   │   └── layout.html
│   │   └── main/
│   │       ├── home.html
│   │       ├── about.html
│   │       ├── article_detail.html
│   │       ├── article_edit.html
│   │       └── article_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
```

Теперь у нас есть полноценный блог с профессиональной структурой шаблонов, статическими файлами и полным набором CRUD операций! В следующем модуле можно добавить пользователей, комментарии и пагинацию.
