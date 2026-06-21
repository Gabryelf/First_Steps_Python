from core.model.postgresql_db import PostgreSQLDB
from core.model.mysql_db import MySQLDB
from core.model.mongodb_db import MongoDB


class UniversalDBManager:
    def __init__(self):
        self.databases = {}
        self.current_db = None

    def add_database(self, db_type, db_instance):
        """Добавление СУБД в менеджер"""
        self.databases[db_type] = db_instance

    def set_current_db(self, db_type):
        """Установка текущей СУБД"""
        if db_type in self.databases:
            self.current_db = self.databases[db_type]
            print(f"Текущая СУБД: {db_type}")
        else:
            print(f"СУБД {db_type} не найдена")

    def get_current_db(self):
        """Получение текущей СУБД"""
        return self.current_db

    def execute_on_all(self, method_name, *args):
        """Выполнение метода на всех СУБД"""
        results = {}
        for db_type, db_instance in self.databases.items():
            print(f"\nВыполняем на {db_type}...")
            method = getattr(db_instance, method_name)
            results[db_type] = method(*args)
        return results


def main():
    db_manager = UniversalDBManager()

    # Инициализируем все СУБД
    print("Инициализация всех СУБД...")

    try:
        db_manager.add_database("PostgreSQL", PostgreSQLDB())
    except Exception as e:
        print(f"PostgreSQL не доступен: {e}")

    try:
        db_manager.add_database("MySQL", MySQLDB())
    except Exception as e:
        print(f"MySQL не доступен: {e}")

    try:
        db_manager.add_database("MongoDB", MongoDB())
    except Exception as e:
        print(f"MongoDB не доступен: {e}")

    # Основной цикл
    while True:
        print("\nУНИВЕРСАЛЬНАЯ СИСТЕМА БАЗ ДАННЫХ")
        print("=" * 40)

        # Показываем доступные СУБД
        available_dbs = list(db_manager.databases.keys())
        print(f"Доступные СУБД: {', '.join(available_dbs)}")

        print("\n1. Выбрать СУБД для работы")
        print("2. Создать структуру во ВСЕХ СУБД")
        print("3. Добавить тестовые данные")
        print("4. Показать все данные")
        print("5. Сравнить СУБД")
        print("6. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            print("\nВыберите СУБД:")
            for i, db_type in enumerate(available_dbs, 1):
                print(f"{i}. {db_type}")

            db_choice = input("Номер СУБД: ")
            try:
                selected_db = available_dbs[int(db_choice) - 1]
                db_manager.set_current_db(selected_db)
            except (ValueError, IndexError):
                print("Неверный выбор")

        elif choice == "2":
            print("\nСоздаем структуру во всех СУБД...")
            db_manager.execute_on_all("create_tables")

        elif choice == "3":
            print("\nДобавляем тестовые данные...")

            # Добавляем жанры
            genres = ["Комедия", "Драма", "Боевик", "Документальный"]
            for genre in genres:
                db_manager.execute_on_all("insert_genre", genre)

            # Добавляем пользователей
            test_users = [
                ("test1@mail.com", "Тест_Пользователь1", "premium"),
                ("test2@mail.com", "Тест_Пользователь2", "basic")
            ]

            for email, username, subscription in test_users:
                db_manager.execute_on_all("insert_user", email, username, subscription)

            print("Тестовые данные добавлены!")

        elif choice == "4":
            current_db = db_manager.get_current_db()
            if current_db:
                print(f"\nДанные из {current_db.get_db_type()}:")
                tables = ["users", "genres", "videos"]
                for table in tables:
                    current_db.show_data(table)
                    input("Нажмите Enter для продолжения...")
            else:
                print("❌ Сначала выберите СУБД")

        elif choice == "5":
            print("\nСРАВНЕНИЕ СУБД:")
            tables = ["users", "genres"]
            for table in tables:
                print(f"\n=== {table.upper()} ===")
                for db_type, db_instance in db_manager.databases.items():
                    print(f"\n{db_type}:")
                    db_instance.show_data(table)

        elif choice == "6":
            print("До свидания!")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()