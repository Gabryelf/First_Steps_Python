# Острова и мосты между ними (как граф)
islands = {
    'остров1': ['остров2', 'остров3'],
    'остров2': ['остров1', 'остров3', 'остров4'],
    'остров3': ['остров1', 'остров2', 'остров4'],
    'остров4': ['остров2', 'остров3']
}


def find_bridge_path():
    """Ищем путь, проходящий по каждому мосту ровно один раз"""
    # Считаем степени вершин (сколько мостов из каждого острова)
    degrees = {}
    for island in islands:
        degrees[island] = len(islands[island])

    print("🌉 Ищем путь по всем мостам...")
    print(f"Степени островов: {degrees}")

    # Проверяем условие эйлерова пути
    odd_vertices = [island for island, deg in degrees.items() if deg % 2 == 1]

    if len(odd_vertices) == 0:
        print("✅ Можно начать с любого острова и вернуться обратно")
        return "Эйлеров цикл"
    elif len(odd_vertices) == 2:
        print(f"✅ Можно начать с {odd_vertices[0]} и закончить в {odd_vertices[1]}")
        return f"Путь {odd_vertices[0]} → {odd_vertices[1]}"
    else:
        print("❌ Нельзя пройти по всем мостам ровно один раз")
        return None


# Играем
find_bridge_path()