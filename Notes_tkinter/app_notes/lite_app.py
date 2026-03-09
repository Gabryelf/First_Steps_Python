notes = []
next_id = 1


def show_menu():
    """Показывает меню программы"""
    print("\n" + "=" * 30)
    print("МОИ ЗАМЕТКИ")
    print("=" * 30)
    print("1. Показать все заметки")
    print("2. Добавить заметку")
    print("3. Посмотреть заметку")
    print("4. Удалить заметку")
    print("0. Выход")
    print("=" * 30)


def show_all_notes():
    """Показывает список всех заметок"""
    if len(notes) == 0:
        print("\nУ вас пока нет заметок.")
        return

    print("\n--- СПИСОК ЗАМЕТОК ---")
    for note in notes:
        print(f"[{note['id']}] {note['title']}")


def add_note():
    """Добавляет новую заметку"""
    global next_id

    print("\n--- НОВАЯ ЗАМЕТКА ---")
    title = input("Заголовок: ")
    content = input("Содержание: ")

    # Создаём заметку (словарь)
    note = {
        'id': next_id,
        'title': title,
        'content': content
    }

    # Добавляем в список
    notes.append(note)
    next_id = next_id + 1

    print(f"✓ Заметка '{title}' добавлена!")


def view_note():
    """Показывает одну заметку по ID"""
    show_all_notes()

    if len(notes) == 0:
        return

    # Просим ввести ID
    id_str = input("\nВведите номер заметки: ")

    # Проверяем, что ввели число
    if not id_str.isdigit():
        print("✗ Ошибка: нужно ввести число!")
        return

    note_id = int(id_str)

    # Ищем заметку
    found = False
    for note in notes:
        if note['id'] == note_id:
            print("\n" + "=" * 30)
            print(f"ЗАМЕТКА №{note['id']}")
            print(f"Заголовок: {note['title']}")
            print("-" * 30)
            print(f"{note['content']}")
            print("=" * 30)
            found = True
            break

    if not found:
        print(f"✗ Заметка с номером {note_id} не найдена!")


def delete_note():
    """Удаляет заметку по ID"""
    show_all_notes()

    if len(notes) == 0:
        return

    id_str = input("\nВведите номер заметки для удаления: ")

    if not id_str.isdigit():
        print("✗ Ошибка: нужно ввести число!")
        return

    note_id = int(id_str)

    # Ищем и удаляем
    for i in range(len(notes)):
        if notes[i]['id'] == note_id:
            title = notes[i]['title']

            # Спрашиваем подтверждение
            confirm = input(f"Удалить заметку '{title}'? (да/нет): ")
            if confirm.lower() in ['да', 'д', 'yes', 'y']:
                notes.pop(i)
                print(f"✓ Заметка удалена!")
            else:
                print("Удаление отменено.")
            return

    print(f"✗ Заметка с номером {note_id} не найдена!")


# --- ГЛАВНАЯ ПРОГРАММА ---
print("ДОБРО ПОЖАЛОВАТЬ В ПРОГРАММУ ЗАМЕТОК!")

# Добавим пару примеров для теста
notes.append({'id': next_id, 'title': 'Купить продукты', 'content': 'Молоко, хлеб, яйца'})
next_id = next_id + 1
notes.append({'id': next_id, 'title': 'Забрать посылку', 'content': 'Пункт выдачи до 20:00'})
next_id = next_id + 1

while True:
    show_menu()
    choice = input("Выберите действие: ")

    if choice == '1':
        show_all_notes()
    elif choice == '2':
        add_note()
    elif choice == '3':
        view_note()
    elif choice == '4':
        delete_note()
    elif choice == '0':
        print("До свидания!")
        break
    else:
        print("✗ Неверный выбор. Попробуйте снова.")

    input("\nНажмите Enter, чтобы продолжить...")