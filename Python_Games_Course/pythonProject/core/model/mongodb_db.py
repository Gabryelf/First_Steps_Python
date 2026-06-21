from pymongo import MongoClient
from datetime import datetime
from util.config import DATABASES
from core.base.database_base import DatabaseInterface


class MongoDB(DatabaseInterface):
    def __init__(self):
        self.client = None
        self.db = None
        self.db_type = "MongoDB"
        self.connect()

    def connect(self):
        try:
            self.client = MongoClient(
                DATABASES["mongodb"]["host"],
                DATABASES["mongodb"]["port"]
            )
            self.db = self.client[DATABASES["mongodb"]["database"]]
            print("Успешное подключение к MongoDB")
        except Exception as e:
            print(f"Ошибка подключения к MongoDB: {e}")

    def create_tables(self):
        try:
            # В MongoDB коллекции создаются автоматически при первой вставке
            collections = ["users", "genres", "videos"]
            for collection in collections:
                if collection not in self.db.list_collection_names():
                    self.db.create_collection(collection)
                    print(f"Коллекция создана в MongoDB: {collection}")
            return True
        except Exception as e:
            print(f"Ошибка создания коллекций в MongoDB: {e}")
            return False

    def insert_user(self, email, username, subscription_type='basic'):
        try:
            user_data = {
                "email": email,
                "username": username,
                "subscription_type": subscription_type,
                "registration_date": datetime.now()
            }

            result = self.db.users.insert_one(user_data)
            print(f"Пользователь добавлен в MongoDB: {username}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"Ошибка добавления пользователя в MongoDB: {e}")
            return None

    def insert_genre(self, name):
        try:
            genre_data = {
                "name": name,
                "created_at": datetime.now()
            }

            # Используем upsert для избежания дубликатов
            result = self.db.genres.update_one(
                {"name": name},
                {"$setOnInsert": genre_data},
                upsert=True
            )

            print(f"Жанр добавлен в MongoDB: {name}")
            return result.upserted_id
        except Exception as e:
            print(f"Ошибка добавления жанра в MongoDB: {e}")
            return None

    def insert_video(self, title, description, duration, user_id, genre_ids=None):
        try:
            video_data = {
                "title": title,
                "description": description,
                "duration": duration,
                "user_id": user_id,
                "genres": genre_ids or [],
                "upload_date": datetime.now()
            }

            result = self.db.videos.insert_one(video_data)
            print(f"Видео добавлено в MongoDB: {title}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"Ошибка добавления видео в MongoDB: {e}")
            return None

    def show_data(self, collection_name):
        try:
            documents = list(self.db[collection_name].find())

            print(f"\nMongoDB - {collection_name}:")
            for doc in documents:
                # Преобразуем ObjectId в строку для читаемости
                readable_doc = {k: (str(v) if k == '_id' else v) for k, v in doc.items()}
                print(f"  {readable_doc}")

            return documents
        except Exception as e:
            print(f"Ошибка чтения данных из MongoDB: {e}")
            return []

    def get_db_type(self):
        return self.db_type










# Идеально для:
# - Быстрое прототипирование
# - Гибкие схемы данных
# - Большие объемы записи
# - Контент-ориентированные приложения
# - Масштабирование на множество серверов