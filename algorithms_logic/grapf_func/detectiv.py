# Социальная сеть (кто с кем знаком)
people = {
    'Анна': ['Борис', 'Виктор'],
    'Борис': ['Анна', 'Галина', 'Дмитрий'],
    'Виктор': ['Анна', 'Галина'],
    'Галина': ['Борис', 'Виктор', 'Елена'],
    'Дмитрий': ['Борис'],
    'Елена': ['Галина']
}


def find_connection(person1, person2):
    """Находим связь между двумя людьми через общих знакомых"""
    print(f"🔍 Ищем связь между {person1} и {person2}")

    # Проверяем прямую связь
    if person2 in people[person1]:
        print(f"✅ Прямая связь: {person1} знаком с {person2}")
        return True

    # Ищем через одного общего друга
    for friend in people[person1]:
        if person2 in people[friend]:
            print(f"✅ Связь через общего друга: {person1} → {friend} → {person2}")
            return True

    # Ищем через двух друзей
    for friend1 in people[person1]:
        for friend2 in people[friend1]:
            if person2 in people[friend2]:
                print(f"✅ Связь: {person1} → {friend1} → {friend2} → {person2}")
                return True

    print(f"❌ Связи не найдено")
    return False


# Играем
find_connection('Анна', 'Елена')