from library_db import LibraryDB


def main():
    library = LibraryDB()

    print("ДОБАВЛЯЕМ ТЕСТОВЫЕ ДАННЫЕ...")

    books = [
        ("Война и мир", "Лев Толстой", 1869, "Роман"),
        ("Преступление и наказание", "Федор Достоевский", 1866, "Роман"),
        ("Мастер и Маргарита", "Михаил Булгаков", 1967, "Фэнтези"),
        ("1984", "Джордж Оруэлл", 1949, "Антиутопия"),
        ("Гарри Поттер и философский камень", "Джоан Роулинг", 1997, "Фэнтези")
    ]

    for book in books:
        library.add_book(*book)

    readers = [
        ("Анна Иванова", "anna@mail.com", "+79161234567"),
        ("Петр Сидоров", "petr@mail.com", "+79167654321"),
        ("Мария Петрова", "maria@mail.com", None)
    ]

    for reader in readers:
        library.add_reader(*reader)

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ БИБЛИОТЕКИ")
    print("=" * 50)

    while True:
        print("\n1. Показать все книги")
        print("2. Показать всех читателей")
        print("3. Показать текущие выдачи")
        print("4. Выдать книгу")
        print("5. Вернуть книгу")
        print("6. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            library.show_books()

        elif choice == "2":
            library.show_readers()

        elif choice == "3":
            library.show_current_loans()

        elif choice == "4":
            library.show_books()
            library.show_readers()

            try:
                book_id = int(input("\nID книги для выдачи: "))
                reader_id = int(input("ID читателя: "))
                library.lend_book(book_id, reader_id)
            except ValueError:
                print("Ошибка: введите числа для ID")

        elif choice == "5":
            library.show_current_loans()

            try:
                loan_id = int(input("\nID выдачи для возврата: "))
                library.return_book(loan_id)
            except ValueError:
                print("Ошибка: введите число для ID выдачи")

        elif choice == "6":
            print("До свидания!")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()