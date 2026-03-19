from decorators import log_action
import storage
import utils

notes = []
next_id = 1


def show_menu():
    """Показывает меню"""
    print("\n" + "=" * 30)
    print("МОИ ЗАМЕТКИ")
    print("=" * 30)
    print("1. Показать все заметки")
    print("2. Добавить заметку")
    print("3. Посмотреть заметку")
    print("4. Удалить заметку")
    print("0. Выход")
    print("=" * 30)


@log_action
def show_all_notes():
    """Показывает все заметки"""
    if not notes:
        print("\nУ вас пока нет заметок.")
        return

    print("\n--- СПИСОК ЗАМЕТОК ---")
    for note in notes:
        print(f"[{note['id']}] {note['title']}")


@log_action
def add_note():
    """Добавляет заметку"""
    global next_id

    print("\n--- НОВАЯ ЗАМЕТКА ---")
    title = input("Заголовок: ")
    content = input("Содержание: ")

    note = {
        'id': next_id,
        'title': title,
        'content': content
    }

    notes.append(note)
    next_id += 1
    storage.save_notes(notes)
    print(f"✓ Заметка добавлена!")


@log_action
def view_note():
    """Показывает одну заметку"""
    show_all_notes()

    if not notes:
        return

    try:
        note_id = int(input("\nВведите номер заметки: "))

        for note in notes:
            if note['id'] == note_id:
                print(f"\nЗаголовок: {note['title']}")
                print(f"Содержание: {note['content']}")
                return

        print("Заметка не найдена!")
    except ValueError:
        print("Ошибка! Нужно ввести число.")


@log_action
def delete_note():
    show_all_notes()

    if not notes:
        return

    try:
        note_id = int(input("\nВведите номер заметки для удаления: "))

        for i, note in enumerate(notes):
            if note['id'] == note_id:
                confirm = input(f"Удалить '{note['title']}'? (да/нет): ")
                if confirm.lower() in ['да', 'д', 'yes', 'y']:
                    notes.pop(i)
                    storage.save_notes(notes)
                    print("✓ Заметка удалена!")
                else:
                    print("Удаление отменено.")
                return

        print("Заметка не найдена!")
    except ValueError:
        print("Ошибка! Нужно ввести число.")



notes = storage.load_notes()
if notes:
    next_id = max(note['id'] for note in notes) + 1
    print(f"Загружено {len(notes)} заметок")
else:
    # Добавляем примеры для первого запуска
    notes = [
        {'id': 1, 'title': 'Купить продукты', 'content': 'Молоко, хлеб'},
        {'id': 2, 'title': 'Позвонить маме', 'content': 'Вечером'}
    ]
    next_id = 3
    storage.save_notes(notes)

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
        print("Неверный выбор!")

    utils.pause()
    utils.clear_screen()
    