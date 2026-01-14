from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article


def home(request):
    # Получаем все статьи из базы данных
    articles = Article.objects.all()

    # Если форма была отправлена (POST-запрос)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем статью в базу данных
            return redirect('home')  # Перенаправляем на главную
    else:
        form = ArticleForm()  # Создаем пустую форму для GET-запроса

    # Передаем статьи и форму в шаблон
    return render(request, 'main/home.html', {
        'articles': articles,
        'form': form
    })

