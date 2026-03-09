""""""


class Note:
    """Класс, представляющий одну заметку"""

    def __init__(self, note_id, title, content):
        self.id = note_id
        self.title = title
        self.content = content

    def __str__(self):
        """Строковое представление заметки"""
        return f"[{self.id}] {self.title}\n{self.content}\n"


class NoteManager:
    """Класс для управления заметками"""

    def __init__(self):
        self.notes = []  # список заметок
        self.next_id = 1  # для генерации ID

    def add_note(self, title, content):
        """Добавить новую заметку"""
        note = Note(self.next_id, title, content)
        self.notes.append(note)
        self.next_id += 1
        return note

    def get_all_notes(self):
        """Получить все заметки"""
        return self.notes

    def find_note_by_id(self, note_id):
        """Найти заметку по ID"""
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def delete_note(self, note_id):
        """Удалить заметку по ID"""
        note = self.find_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            return True
        return False

    def update_note(self, note_id, title, content):
        """Обновить заметку"""
        note = self.find_note_by_id(note_id)
        if note:
            note.title = title
            note.content = content
            return True
        return False


class ConsoleApp:
    """Консольный интерфейс приложения"""

    def __init__(self):
        self.manager = NoteManager()

    def show_menu(self):
        """Показать меню"""
        print("\n" + "=" * 40)
        print("МЕНЮ ЗАМЕТОК:")
        print("1. Показать все заметки")
        print("2. Добавить заметку")
        print("3. Просмотреть заметку")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("0. Выход")
        print("=" * 40)

    def show_all_notes(self):
        """Показать все заметки"""
        notes = self.manager.get_all_notes()
        if not notes:
            print("\nУ вас пока нет заметок.")
            return

        print("\n" + "-" * 40)
        print("СПИСОК ЗАМЕТОК:")
        for note in notes:
            print(f"[{note.id}] {note.title}")
        print("-" * 40)

    def add_note(self):
        """Добавить новую заметку"""
        print("\n--- Новая заметка ---")
        title = input("Введите заголовок: ")
        content = input("Введите содержание: ")

        note = self.manager.add_note(title, content)
        print(f"✓ Заметка '{note.title}' (ID: {note.id}) добавлена!")

    def view_note(self):
        """Просмотреть конкретную заметку"""
        self.show_all_notes()

        try:
            note_id = int(input("\nВведите ID заметки: "))
            note = self.manager.find_note_by_id(note_id)

            if note:
                print("\n" + "=" * 40)
                print(f"ЗАМЕТКА #{note.id}")
                print(f"Заголовок: {note.title}")
                print("-" * 40)
                print(f"Содержание:\n{note.content}")
                print("=" * 40)
            else:
                print(f"✗ Заметка с ID {note_id} не найдена.")
        except ValueError:
            print("✗ Ошибка: введите число!")

    def edit_note(self):
        """Редактировать заметку"""
        self.show_all_notes()

        try:
            note_id = int(input("\nВведите ID заметки для редактирования: "))
            note = self.manager.find_note_by_id(note_id)

            if note:
                print(f"Редактирование заметки '{note.title}'")
                print("(оставьте поле пустым, чтобы оставить текущее значение)")

                new_title = input(f"Заголовок [{note.title}]: ")
                new_content = input(f"Содержание [{note.content}]: ")

                # Если пользователь ничего не ввел, оставляем старое значение
                title = new_title if new_title else note.title
                content = new_content if new_content else note.content

                self.manager.update_note(note_id, title, content)
                print(f"✓ Заметка #{note_id} обновлена!")
            else:
                print(f"✗ Заметка с ID {note_id} не найдена.")
        except ValueError:
            print("✗ Ошибка: введите число!")

    def delete_note(self):
        """Удалить заметку"""
        self.show_all_notes()

        try:
            note_id = int(input("\nВведите ID заметки для удаления: "))

            # Запрос подтверждения
            confirm = input(f"Удалить заметку #{note_id}? (д/н): ")

            if confirm.lower() in ['д', 'да', 'y', 'yes']:
                if self.manager.delete_note(note_id):
                    print(f"✓ Заметка #{note_id} удалена!")
                else:
                    print(f"✗ Заметка с ID {note_id} не найдена.")
        except ValueError:
            print("✗ Ошибка: введите число!")

    def run(self):
        """Запуск приложения"""
        print("ДОБРО ПОЖАЛОВАТЬ В ПРИЛОЖЕНИЕ ЗАМЕТОК!")

        while True:
            self.show_menu()
            choice = input("Выберите действие: ")

            if choice == '1':
                self.show_all_notes()
            elif choice == '2':
                self.add_note()
            elif choice == '3':
                self.view_note()
            elif choice == '4':
                self.edit_note()
            elif choice == '5':
                self.delete_note()
            elif choice == '0':
                print("До свидания!")
                break
            else:
                print("✗ Неверный выбор. Попробуйте снова.")


# Точка входа
if __name__ == "__main__":
    app = ConsoleApp()
    app.run()
