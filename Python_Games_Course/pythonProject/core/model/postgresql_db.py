import psycopg2
from psycopg2 import sql
from util.config import DATABASES, SQL_TEMPLATES
from core.base.database_base import DatabaseInterface


class PostgreSQLDB(DatabaseInterface):
    def __init__(self):
        self.conn = None
        self.db_type = "PostgreSQL"
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(**DATABASES["postgresql"])
            print("Успешное подключение к PostgreSQL")
        except Exception as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")

    def create_tables(self):
        try:
            cur = self.conn.cursor()
            for table_name, create_sql in SQL_TEMPLATES.items():
                cur.execute(create_sql)
                print(f"Таблица создана: {table_name}")

            self.conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Ошибка создания таблиц: {e}")
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
            print(f"Пользователь добавлен в PostgreSQL: {username}")
            return True
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")
            return False

    def insert_genre(self, name):
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO genres (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                (name,)
            )
            self.conn.commit()
            cur.close()
            print(f"Жанр добавлен в PostgreSQL: {name}")
            return True
        except Exception as e:
            print(f"Ошибка добавления жанра: {e}")
            return False

    def insert_video(self, title, description, duration, user_id, genre_ids=None):
        try:
            cur = self.conn.cursor()

            cur.execute(
                """INSERT INTO videos (title, description, duration, user_id) 
                VALUES (%s, %s, %s, %s) RETURNING video_id""",
                (title, description, duration, user_id)
            )
            video_id = cur.fetchone()[0]

            if genre_ids:
                for genre_id in genre_ids:
                    cur.execute(
                        "INSERT INTO video_genres (video_id, genre_id) VALUES (%s, %s)",
                        (video_id, genre_id)
                    )

            self.conn.commit()
            cur.close()
            print(f"Видео добавлено в PostgreSQL: {title}")
            return video_id
        except Exception as e:
            print(f"Ошибка добавления видео: {e}")
            self.conn.rollback()
            return None

    def show_data(self, table_name):
        try:
            cur = self.conn.cursor()
            cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            rows = cur.fetchall()

            print(f"\nPostgreSQL - {table_name}:")
            for row in rows:
                print(f"  {row}")

            cur.close()
            return rows
        except Exception as e:
            print(f"Ошибка чтения данных: {e}")
            return []

    def get_db_type(self):
        return self.db_type









# Идеально для:
# - Сложные бизнес-правила
# - Транзакционные операции
# - Геоданные (PostGIS)
# - JSON + реляционные данные
# - Целостность данных критична