# test_connection.py в корне server
import pymysql
import time


def test_connection():
    print("🔍 Тестирование подключения к MySQL...")

    configs = [
        {"host": "localhost", "port": 3306, "user": "root", "password": "rootpassword", "db": "idle_tower_defense"},
        {"host": "mysql", "port": 3306, "user": "root", "password": "rootpassword", "db": "idle_tower_defense"}
    ]

    for config in configs:
        try:
            print(f"Попытка подключения к {config['host']}:{config['port']}...")
            connection = pymysql.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['db'],
                connect_timeout=5
            )

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                print(f"✅ Успешное подключение к {config['host']}! Результат: {result}")

            connection.close()
            return True

        except Exception as e:
            print(f"❌ Не удалось подключиться к {config['host']}: {e}")

    return False


if __name__ == "__main__":
    test_connection()