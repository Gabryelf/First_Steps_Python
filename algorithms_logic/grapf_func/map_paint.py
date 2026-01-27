# Страны на карте (соседи не могут иметь один цвет)
countries = {
    'россия': ['китай', 'казахстан', 'украина'],
    'китай': ['россия', 'казахстан'],
    'казахстан': ['россия', 'китай', 'узбекистан'],
    'узбекистан': ['казахстан'],
    'украина': ['россия']
}

colors = ['🔴', '🟢', '🔵', '🟡']  # доступные цвета


def color_map():
    """Раскрашиваем карту так, чтобы соседи не были одного цвета"""
    colored = {}

    print("🎨 Раскрашиваем карту...")

    for country in countries:
        # Цвета соседей этой страны
        neighbor_colors = set()
        for neighbor in countries[country]:
            if neighbor in colored:
                neighbor_colors.add(colored[neighbor])

        # Выбираем первый доступный цвет
        for color in colors:
            if color not in neighbor_colors:
                colored[country] = color
                print(f"  {country}: {color}")
                break
        else:
            print(f"❌ Не могу раскрасить {country}")
            return None

    print("\n✅ Карта раскрашена!")
    return colored


# Играем
color_map()