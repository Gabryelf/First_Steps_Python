import psycopg2
import sys


class LibraryDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="library",
            user="postgres",
            password="postgres"
        )
        self.create_tables()

    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                author VARCHAR(100) NOT NULL, 
                year INTEGER,
                genre VARCHAR(50),
                is_available BOOLEAN DEFAULT TRUE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS readers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE,
                phone VARCHAR(20)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS book_loans (
                id SERIAL PRIMARY KEY,
                book_id INTEGER REFERENCES books(id),
                reader_id INTEGER REFERENCES readers(id),
                loan_date DATE DEFAULT CURRENT_DATE,
                return_date DATE,
                returned BOOLEAN DEFAULT FALSE
            )
            """
        )

        cur = self.conn.cursor()
        for command in commands:
            cur.execute(command)
        self.conn.commit()
        cur.close()
        print("Таблицы созданы!")

    def add_book(self, title, author, year=None, genre=None):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, year, genre) VALUES (%s, %s, %s, %s)",
            (title, author, year, genre)
        )
        self.conn.commit()
        cur.close()
        print(f"Книга добавлена: '{title}'")

    def add_reader(self, name, email=None, phone=None):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO readers (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        self.conn.commit()
        cur.close()
        print(f"Читатель добавлен: {name}")

    def lend_book(self, book_id, reader_id):
        cur = self.conn.cursor()

        # Проверяем, доступна ли книга
        cur.execute("SELECT is_available FROM books WHERE id = %s", (book_id,))
        result = cur.fetchone()

        if not result or not result[0]:
            print("Книга недоступна для выдачи")
            return False

        # Выдаем книгу
        cur.execute(
            "INSERT INTO book_loans (book_id, reader_id) VALUES (%s, %s)",
            (book_id, reader_id)
        )

        # Помечаем книгу как недоступную
        cur.execute(
            "UPDATE books SET is_available = FALSE WHERE id = %s",
            (book_id,)
        )

        self.conn.commit()
        cur.close()
        print("Книга выдана читателю")
        return True

    def return_book(self, loan_id):
        cur = self.conn.cursor()

        # Находим book_id по loan_id
        cur.execute("SELECT book_id FROM book_loans WHERE id = %s", (loan_id,))
        result = cur.fetchone()

        if not result:
            print("Запись о выдаче не найдена")
            return False

        book_id = result[0]

        # Обновляем запись о выдаче
        cur.execute(
            "UPDATE book_loans SET returned = TRUE, return_date = CURRENT_DATE WHERE id = %s",
            (loan_id,)
        )

        # Делаем книгу доступной
        cur.execute(
            "UPDATE books SET is_available = TRUE WHERE id = %s",
            (book_id,)
        )

        self.conn.commit()
        cur.close()
        print("Книга возвращена в библиотеку")
        return True

    def show_books(self):
        """Показать все книги"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, title, author, year, genre, 
                   CASE WHEN is_available THEN 'Доступна' ELSE 'Выдана' END as status
            FROM books 
            ORDER BY title
        """)

        print("\nКНИГИ В БИБЛИОТЕКЕ:")
        print("-" * 60)
        for row in cur.fetchall():
            print(f"ID: {row[0]} | {row[1]} - {row[2]} ({row[3]}) | {row[4]} | {row[5]}")

        cur.close()

    def show_readers(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, email, phone FROM readers ORDER BY name")

        print("\nЧИТАТЕЛИ:")
        print("-" * 40)
        for row in cur.fetchall():
            print(f"ID: {row[0]} | {row[1]} | {row[2]} | {row[3]}")

        cur.close()

    def show_current_loans(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT bl.id, b.title, r.name, bl.loan_date
            FROM book_loans bl
            JOIN books b ON bl.book_id = b.id
            JOIN readers r ON bl.reader_id = r.id
            WHERE bl.returned = FALSE
            ORDER BY bl.loan_date
        """)

        print("\nТЕКУЩИЕ ВЫДАЧИ:")
        print("-" * 50)
        for row in cur.fetchall():
            print(f"ID выдачи: {row[0]} | Книга: {row[1]} | Читатель: {row[2]} | Дата: {row[3]}")

        cur.close()


# Создаем экземпляр базы данных
library = LibraryDB()