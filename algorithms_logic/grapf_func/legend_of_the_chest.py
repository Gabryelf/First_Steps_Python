# Игра: найди сундук в лабиринте комнат
rooms = {
    'старт': ['коридор', 'кухня'],
    'коридор': ['старт', 'спальня', 'кладовая'],
    'кухня': ['старт', 'столовая'],
    'спальня': ['коридор'],
    'кладовая': ['коридор', 'тайная_комната'],  # здесь сундук!
    'столовая': ['кухня'],
    'тайная_комната': ['кладовая']
}


def find_treasure(start_room):
    """Ищем сундук обходом в ширину (BFS)"""
    from collections import deque

    queue = deque([start_room])
    visited = set()
    path = []

    print("🔍 Ищем сундук...")

    while queue:
        room = queue.popleft()

        if room in visited:
            continue

        visited.add(room)
        path.append(room)

        print(f"  Зашли в: {room}")

        # Нашли сундук!
        if room == 'тайная_комната':
            print(f"🎉 НАШЛИ СУНДУК! Путь: {' → '.join(path)}")
            return True

        # Добавляем соседние комнаты
        for neighbor in rooms[room]:
            if neighbor not in visited:
                queue.append(neighbor)

    print("💔 Сундук не найден")
    return False


# Играем
find_treasure('старт')