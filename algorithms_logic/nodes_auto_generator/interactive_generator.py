# interactive_generator.py
from config import TEMPLATES, STYLES

print("🎨 ГЕНЕРАТОР САЙТОВ")
print("=" * 30)

# 1. Выбираем шаблон
print("\nДоступные шаблоны:")
for name in TEMPLATES.keys():
    print(f"  - {name}")

template = input("\nВыберите шаблон: ")

# 2. Выбираем стиль
print("\nДоступные стили:")
for name in STYLES.keys():
    print(f"  - {name}")

style = input("\nВыберите стиль: ")

# 3. Заполняем контент
print("\n📝 Заполните контент:")
variables = {}
for key in ["title", "header", "content"]:
    value = input(f"{key}: ")
    variables[key] = value

