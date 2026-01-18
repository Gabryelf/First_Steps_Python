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