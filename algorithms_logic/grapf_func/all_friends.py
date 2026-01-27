graph = {
    'Аня': ['Боря', 'Ваня', 'Галя'],
    'Боря': ['Аня', 'Дима'],
    'Ваня': ['Аня'],
    'Галя': ['Аня', 'Егор'],
    'Дима': ['Боря'],
    'Егор': ['Галя']
}


def get_friends(name):
    """Получаем всех друзей человека"""
    return graph[name]


def common_friends(name1, name2):
    """Находим общих друзей двух людей"""
    friends1 = set(graph[name1])  # делаем множества
    friends2 = set(graph[name2])

    common = friends1 & friends2  # пересечение множеств

    if common:
        print(f"Общие друзья {name1} и {name2}: {list(common)}")
    else:
        print(f"У {name1} и {name2} нет общих друзей")

    return common


common_friends('Аня', 'Боря')
common_friends('Аня', 'Дима')

#print("Друзья Ани:", get_friends('Аня'))
#print("Друзья Бори:", get_friends('Боря'))