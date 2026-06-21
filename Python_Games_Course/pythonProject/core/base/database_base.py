from abc import ABC, abstractmethod


class DatabaseInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def insert_user(self, email, username, subscription_type='basic'):
        pass

    @abstractmethod
    def insert_genre(self, name):
        pass

    @abstractmethod
    def insert_video(self, title, description, duration, user_id, genre_ids=None):
        pass

    @abstractmethod
    def show_data(self, table_name):
        pass

    @abstractmethod
    def get_db_type(self):
        pass