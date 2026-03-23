def clear_screen():
    """Очищает экран"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Ждет нажатия Enter"""
    input("Нажмите Enter чтобы продолжить...")