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