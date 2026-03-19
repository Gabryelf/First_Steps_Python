def log_action(func):
    """Простой декоратор для логирования"""
    def wrapper(*args, **kwargs):
        print(f"→ Выполняется действие: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"← Действие завершено")
        return result
    return wrapper
