# Известная теория: любые два человека на Земле
# связаны через 6 или менее знакомств

def check_connection(graph, start, end, steps=0, maximum=6):
    # Базовый случай: мы нашли человека
    if start == end:
        return True, steps

    # Базовый случай: слишком много шагов
    if steps >= maximum:
        return False, steps

    # Рекурсивно проверяем всех друзей
    for friend in graph.get(start, []):
        find, count = check_connection(graph, friend, end, steps + 1, maximum)
        if find:
            return True, count

    return False, steps


# Тест
test_graph = {
    "Я": ["Мама", "Лучший_друг"],
    "Мама": ["Я", "Коллега"],
    "Лучший_друг": ["Я", "Друг_из_школы"],
    "Коллега": ["Мама", "Знакомый"],
    "Друг_из_школы": ["Лучший_друг", "Незнакомец"],
    "Знакомый": ["Коллега"],
    "Незнакомец": ["Друг_из_школы"]
}

result, steps = check_connection(test_graph, "Я", "Друг_из_школы")
if result:
    print(f"Связаны через {steps} шагов!")
else:
    print("Не связаны за 6 шагов")