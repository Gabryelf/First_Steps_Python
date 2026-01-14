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