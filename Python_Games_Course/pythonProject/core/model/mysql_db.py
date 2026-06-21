import mysql.connector
from util.config import DATABASES, MYSQL_TEMPLATES
from core.base.database_base import DatabaseInterface


class MySQLDB(DatabaseInterface):
    def __init__(self):
        self.conn = None
        self.db_type = "MySQL"
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**DATABASES["mysql"])
            print("Успешное подключение к MySQL")
        except Exception as e:
            print(f"Ошибка подключения к MySQL: {e}")

    def create_tables(self):
        try:
            cur = self.conn.cursor()

            # Создаем таблицы в правильном порядке из-за foreign keys
            tables_order = ["users", "genres", "videos", "video_genres"]

            for table_name in tables_order:
                if table_name in MYSQL_TEMPLATES:
                    cur.execute(MYSQL_TEMPLATES[table_name])
                    print(f"Таблица создана в MySQL: {table_name}")

            self.conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Ошибка создания таблиц в MySQL: {e}")
            return False

    def insert_user(self, email, username, subscription_type='basic'):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO users (email, username, subscription_type) VALUES (%s, %s, %s)",
                (email, username, subscription_type)
            )
            self.conn.commit()
            cur.close()
            print(f"Пользователь добавлен в MySQL: {username}")
            return True
        except Exception as e:
            print(f"Ошибка добавления пользователя в MySQL: {e}")
            return False

    def insert_genre(self, name):
        """Добавление жанра в MySQL"""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT IGNORE INTO genres (name) VALUES (%s)",
                (name,)
            )
            self.conn.commit()
            cur.close()
            print(f"Жанр добавлен в MySQL: {name}")
            return True
        except Exception as e:
            print(f"Ошибка добавления жанра в MySQL: {e}")
            return False

    def insert_video(self, title, description, duration, user_id, genre_ids=None):
        try:
            cur = self.conn.cursor()

            cur.execute(
                """INSERT INTO videos (title, description, duration, user_id) 
                VALUES (%s, %s, %s, %s)""",
                (title, description, duration, user_id)
            )
            video_id = cur.lastrowid

            if genre_ids:
                for genre_id in genre_ids:
                    cur.execute(
                        "INSERT IGNORE INTO video_genres (video_id, genre_id) VALUES (%s, %s)",
                        (video_id, genre_id)
                    )

            self.conn.commit()
            cur.close()
            print(f"Видео добавлено в MySQL: {title}")
            return video_id
        except Exception as e:
            print(f"Ошибка добавления видео в MySQL: {e}")
            self.conn.rollback()
            return None

    def show_data(self, table_name):
        try:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()

            print(f"\nMySQL - {table_name}:")
            for row in rows:
                print(f"  {row}")

            cur.close()
            return rows
        except Exception as e:
            print(f"Ошибка чтения данных из MySQL: {e}")
            return []

    def get_db_type(self):
        return self.db_type








# Идеально для:
# - Веб-приложения
# - Простые транзакции
# - Чтение-ориентированные workload
# - Репликация для отказоустойчивости