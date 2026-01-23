from .models import Category


def categories(request):
    """Добавляет категории во все шаблоны"""
    return {
        'categories': Category.objects.all()
    }
