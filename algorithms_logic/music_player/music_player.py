print("🎵 Добро пожаловать в музыкальный плеер!")
print("=" * 40)


# Класс для хранения информации о песне
class Song:
    """
    Класс, представляющий одну песню в плейлисте.
    Хранит название, исполнителя, альбом и длительность.
    """

    def __init__(self, title, artist, album=None, duration=0):
        """
        Конструктор класса Song
        title - название песни (строка)
        artist - исполнитель (строка)
        album - название альбома (строка, необязательно)
        duration - длительность в секундах (число)
        """
        self.title = title  # Название песни
        self.artist = artist  # Исполнитель
        self.album = album  # Альбом (может быть None)
        self.duration = duration  # Длительность в секундах

        # Для связного списка
        self.next_song = None  # Следующая песня
        self.prev_song = None  # Предыдущая песня (для двусвязного списка)

    def __str__(self):
        """Красивый вывод информации о песне"""
        minutes = self.duration // 60
        seconds = self.duration % 60

        if self.album:
            return f"{self.title} - {self.artist} ({self.album}) [{minutes}:{seconds:02d}]"
        else:
            return f"{self.title} - {self.artist} [{minutes}:{seconds:02d}]"

    def play(self):
        """Воспроизведение песни (симуляция)"""
        print(f"\n🎶 Сейчас играет: {self}")
        print("♪♫♬" * 10)


# 📝 Сразу проверяем, как работает класс Song
print("\n🔧 Проверяем класс Song:")
print("-" * 30)

# Создаем несколько песен для примера
song1 = Song("Bohemian Rhapsody", "Queen", "A Night at the Opera", 354)
song2 = Song("Imagine", "John Lennon", None, 183)
song3 = Song("Billie Jean", "Michael Jackson", "Thriller", 294)

# Выводим информацию о песнях
print("Создали песни:")
print(f"1. {song1}")
print(f"2. {song2}")
print(f"3. {song3}")

# Пробуем "воспроизвести" песню
song1.play()


# Продолжаем в том же файле

class Playlist:
    """
    Класс для управления плейлистом.
    Использует двусвязный список для хранения песен.
    """

    def __init__(self, name):
        """
        Конструктор плейлиста
        name - название плейлиста
        """
        self.name = name  # Название плейлиста
        self.head = None  # Первая песня в списке
        self.tail = None  # Последняя песня в списке
        self.current = None  # Текущая играющая песня
        self.length = 0  # Количество песен

    def add_song(self, song):
        """
        Добавляет песню в конец плейлиста
        """
        print(f"\n➕ Добавляем песню: {song.title}")

        if self.head is None:  # Если плейлист пустой
            self.head = song
            self.tail = song
            self.current = song
        else:  # Если в плейлисте уже есть песни
            # Связываем последнюю песню с новой
            self.tail.next_song = song
            # Новая песня ссылается на предыдущую
            song.prev_song = self.tail
            # Новая песня становится последней
            self.tail = song

        self.length += 1
        print(f"✅ В плейлисте теперь {self.length} песен")

    def show_all_songs(self):
        """
        Показывает все песни в плейлисте
        """
        print(f"\n📋 Плейлист '{self.name}':")
        print("-" * 40)

        if self.head is None:
            print("Плейлист пуст 😢")
            return

        current = self.head
        index = 1

        while current is not None:
            prefix = "▶️ " if current == self.current else "  "
            print(f"{prefix}{index}. {current}")
            current = current.next_song
            index += 1

    def play_current(self):
        """
        Воспроизводит текущую песню
        """
        if self.current:
            self.current.play()
        else:
            print("\n❌ Нет текущей песни для воспроизведения")

    def next_song(self):
        """
        Переходит к следующей песне
        """
        if self.current and self.current.next_song:
            self.current = self.current.next_song
            print(f"\n⏭️ Перешли к следующей песне: {self.current.title}")
            return True
        else:
            print("\n⏹️ Это последняя песня в плейлисте")
            return False

    def prev_song(self):
        """
        Возвращается к предыдущей песне
        """
        if self.current and self.current.prev_song:
            self.current = self.current.prev_song
            print(f"\n⏮️ Вернулись к предыдущей песне: {self.current.title}")
            return True
        else:
            print("\n⏹️ Это первая песня в плейлисте")
            return False


# 🧪 Тестируем наш плейлист
print("\n" + "=" * 50)
print("🎯 Тестируем класс Playlist")
print("=" * 50)

# Создаем новый плейлист
my_playlist = Playlist("Мои любимые песни")

# Добавляем песни
my_playlist.add_song(song1)
my_playlist.add_song(song2)
my_playlist.add_song(song3)

# Показываем все песни
my_playlist.show_all_songs()

# Тестируем навигацию
print("\n🔍 Тестируем навигацию по плейлисту:")
print("-" * 30)

my_playlist.play_current()  # Играет первую песню
my_playlist.next_song()  # Переходим к следующей
my_playlist.play_current()  # Играем текущую
my_playlist.prev_song()  # Возвращаемся назад
my_playlist.play_current()  # Играем снова первую


# Продолжаем в том же файле

class TreeNode:
    """
    Узел бинарного дерева поиска для песен
    """

    def __init__(self, song):
        self.song = song  # Песня в узле
        self.left = None  # Левый потомок (песни, которые идут "раньше")
        self.right = None  # Правый потомок (песни, которые идут "позже")

    def __str__(self):
        return str(self.song)


class SongTree:
    """
    Бинарное дерево поиска для быстрого поиска песен по названию
    """

    def __init__(self):
        self.root = None  # Корень дерева

    def insert(self, song):
        """
        Вставляет песню в дерево (по алфавиту названия)
        """
        if self.root is None:
            self.root = TreeNode(song)
        else:
            self._insert_recursive(self.root, song)

    def _insert_recursive(self, node, song):
        """
        Рекурсивная вставка песни в дерево
        """
        # Сравниваем названия песен
        if song.title.lower() < node.song.title.lower():
            # Если новая песня должна быть слева
            if node.left is None:
                node.left = TreeNode(song)
            else:
                self._insert_recursive(node.left, song)
        else:
            # Если новая песня должна быть справа
            if node.right is None:
                node.right = TreeNode(song)
            else:
                self._insert_recursive(node.right, song)

    def search(self, title):
        """
        Ищет песню по названию в дереве
        """
        return self._search_recursive(self.root, title.lower())

    def _search_recursive(self, node, title):
        """
        Рекурсивный поиск песни
        """
        if node is None:
            return None

        if title == node.song.title.lower():
            return node.song
        elif title < node.song.title.lower():
            return self._search_recursive(node.left, title)
        else:
            return self._search_recursive(node.right, title)

    def display_tree(self, level=0, prefix="Корень:"):
        """
        Красиво отображает дерево в консоли
        """
        if self.root is None:
            print("Дерево пустое")
            return

        self._display_recursive(self.root, level, prefix)

    def _display_recursive(self, node, level=0, prefix=""):
        """
        Рекурсивный вывод дерева
        """
        if node is not None:
            indent = "  " * level
            print(f"{indent}{prefix} {node.song.title}")

            if node.left or node.right:
                if node.left:
                    self._display_recursive(node.left, level + 1, "├── L:")
                if node.right:
                    self._display_recursive(node.right, level + 1, "└── R:")


# 🧠 Тестируем дерево поиска
print("\n" + "=" * 50)
print("🌳 Тестируем бинарное дерево поиска")
print("=" * 50)

# Создаем дерево
song_tree = SongTree()

# Добавляем песни в дерево (в другом порядке)
songs_to_add = [
    Song("Hotel California", "Eagles", "Hotel California", 391),
    Song("Like a Rolling Stone", "Bob Dylan", "Highway 61 Revisited", 369),
    Song("Smells Like Teen Spirit", "Nirvana", "Nevermind", 301),
    Song("One", "Metallica", "...And Justice for All", 446),
    Song("Stairway to Heaven", "Led Zeppelin", "Led Zeppelin IV", 482),
]

print("\nДобавляем песни в дерево поиска:")
for song in songs_to_add:
    song_tree.insert(song)
    print(f"  ✓ {song.title}")

# Показываем структуру дерева
print("\n📊 Структура дерева поиска:")
print("-" * 30)
song_tree.display_tree()

# Ищем песни
print("\n🔍 Поиск песен в дереве:")
print("-" * 30)

search_titles = ["One", "Hotel California", "Неизвестная песня"]
for title in search_titles:
    found = song_tree.search(title)
    if found:
        print(f"✅ Найдена: {found}")
    else:
        print(f"❌ Не найдена: {title}")


# Продолжаем в том же файле

class MusicPlayer:
    """
    Основной класс музыкального плеера, который объединяет все компоненты
    """

    def __init__(self):
        """
        Инициализация плеера
        """
        self.playlists = {}  # Словарь плейлистов: {"имя": Playlist}
        self.current_playlist = None  # Текущий плейлист
        self.song_tree = SongTree()  # Дерево для быстрого поиска
        self.all_songs = []  # Все песни для сортировки

        print("🎵 Музыкальный плеер инициализирован!")

    def create_playlist(self, name):
        """
        Создает новый плейлист
        """
        if name in self.playlists:
            print(f"\n❌ Плейлист '{name}' уже существует")
            return None

        new_playlist = Playlist(name)
        self.playlists[name] = new_playlist

        if self.current_playlist is None:
            self.current_playlist = new_playlist

        print(f"\n✅ Создан новый плейлист: '{name}'")
        return new_playlist

    def add_song_to_player(self, song, playlist_name=None):
        """
        Добавляет песню в плеер (во все структуры данных)
        """
        print(f"\n🎵 Добавляем песню в плеер: {song.title}")

        # Добавляем в общий список
        self.all_songs.append(song)

        # Добавляем в дерево поиска
        self.song_tree.insert(song)

        # Добавляем в указанный плейлист
        if playlist_name and playlist_name in self.playlists:
            self.playlists[playlist_name].add_song(song)
        elif self.current_playlist:
            self.current_playlist.add_song(song)

        print("✅ Песня добавлена во все структуры данных")

    def search_song(self, title):
        """
        Ищет песню по названию
        """
        print(f"\n🔍 Ищем песню: '{title}'")

        # Поиск в дереве (быстрый)
        found = self.song_tree.search(title)

        if found:
            print(f"✅ Найдена в дереве: {found}")
            return found
        else:
            # Линейный поиск (медленный, но на всякий случай)
            for song in self.all_songs:
                if title.lower() in song.title.lower():
                    print(f"✅ Найдена линейным поиском: {song}")
                    return song

            print(f"❌ Песня '{title}' не найдена")
            return None

    def sort_songs(self, by="title"):
        """
        Сортирует все песни по разным критериям
        """
        print(f"\n📊 Сортируем песни по: {by}")

        if by == "title":
            sorted_songs = sorted(self.all_songs, key=lambda x: x.title.lower())
        elif by == "artist":
            sorted_songs = sorted(self.all_songs, key=lambda x: x.artist.lower())
        elif by == "duration":
            sorted_songs = sorted(self.all_songs, key=lambda x: x.duration)
        else:
            print(f"❌ Неизвестный критерий сортировки: {by}")
            return

        print(f"\n📋 Отсортированный список ({len(sorted_songs)} песен):")
        print("-" * 40)
        for i, song in enumerate(sorted_songs, 1):
            print(f"{i}. {song}")

    def show_player_info(self):
        """
        Показывает информацию о плеере
        """
        print("\n" + "=" * 50)
        print("📊 ИНФОРМАЦИЯ О ПЛЕЕРЕ")
        print("=" * 50)

        print(f"\n📈 Статистика:")
        print(f"  Всего песен: {len(self.all_songs)}")
        print(f"  Всего плейлистов: {len(self.playlists)}")

        if self.current_playlist:
            print(f"  Текущий плейлист: {self.current_playlist.name}")
            print(f"  Песен в текущем плейлисте: {self.current_playlist.length}")

        print("\n📋 Все плейлисты:")
        for name, playlist in self.playlists.items():
            current = " (текущий)" if playlist == self.current_playlist else ""
            print(f"  - {name}{current}: {playlist.length} песен")


# 🎮 Теперь создаем и тестируем полноценный плеер
print("\n" + "=" * 50)
print("🚀 СОЗДАЕМ ПОЛНОЦЕННЫЙ МУЗЫКАЛЬНЫЙ ПЛЕЕР")
print("=" * 50)

# Создаем плеер
player = MusicPlayer()

# Создаем плейлисты
player.create_playlist("Рок-хиты")
player.create_playlist("Вечерний настрой")
player.create_playlist("Для учебы")

# Меняем текущий плейлист
player.current_playlist = player.playlists["Рок-хиты"]

# Добавляем песни в плеер
rock_songs = [
    Song("Sweet Child O' Mine", "Guns N' Roses", "Appetite for Destruction", 356),
    Song("Back in Black", "AC/DC", "Back in Black", 255),
    Song("Nothing Else Matters", "Metallica", "Metallica", 388),
    Song("Purple Haze", "Jimi Hendrix", "Are You Experienced", 170),
    Song("Wonderwall", "Oasis", "(What's the Story) Morning Glory?", 258),
]

print("\n🎸 Добавляем рок-хиты:")
for song in rock_songs:
    player.add_song_to_player(song, "Рок-хиты")

# Добавляем еще песен в другой плейлист
chill_songs = [
    Song("Blinding Lights", "The Weeknd", "After Hours", 200),
    Song("Levitating", "Dua Lipa", "Future Nostalgia", 203),
]

print("\n🎵 Добавляем поп-хиты:")
for song in chill_songs:
    player.add_song_to_player(song, "Вечерний настрой")

# Показываем информацию о плеере
player.show_player_info()

# Ищем песни
print("\n" + "=" * 50)
print("🔎 ТЕСТИРУЕМ ПОИСК ПЕСЕН")
print("=" * 50)

player.search_song("Sweet Child O' Mine")
player.search_song("Levitating")
player.search_song("Несуществующая песня")

# Сортируем песни
print("\n" + "=" * 50)
print("📊 ТЕСТИРУЕМ СОРТИРОВКУ")
print("=" * 50)

player.sort_songs(by="title")
player.sort_songs(by="artist")
player.sort_songs(by="duration")

# Показываем плейлист
print("\n" + "=" * 50)
print("🎧 ТЕСТИРУЕМ ВОСПРОИЗВЕДЕНИЕ")
print("=" * 50)

player.playlists["Рок-хиты"].show_all_songs()
player.playlists["Рок-хиты"].play_current()
player.playlists["Рок-хиты"].next_song()
player.playlists["Рок-хиты"].play_current()


# В конце файла добавляем интерактивное меню

def interactive_menu():
    """
    Интерактивное меню для работы с музыкальным плеером
    """
    player = MusicPlayer()

    # Предварительно создаем плейлист и добавляем песни
    player.create_playlist("Мои хиты")

    sample_songs = [
        Song("Shape of You", "Ed Sheeran", "÷", 233),
        Song("Bad Guy", "Billie Eilish", "When We All Fall Asleep", 194),
        Song("Uptown Funk", "Mark Ronson ft. Bruno Mars", "Uptown Special", 270),
        Song("Rolling in the Deep", "Adele", "21", 228),
        Song("Havana", "Camila Cabello", "Camila", 217),
    ]

    for song in sample_songs:
        player.add_song_to_player(song, "Мои хиты")

    while True:
        print("\n" + "=" * 50)
        print("🎵 МУЗЫКАЛЬНЫЙ ПЛЕЕР - ГЛАВНОЕ МЕНЮ")
        print("=" * 50)
        print("1. 📋 Показать текущий плейлист")
        print("2. ▶️ Воспроизвести текущую песню")
        print("3. ⏭️ Следующая песня")
        print("4. ⏮️ Предыдущая песня")
        print("5. 🔍 Найти песню по названию")
        print("6. 📊 Отсортировать песни")
        print("7. 🎵 Добавить новую песню")
        print("8. 📈 Показать статистику")
        print("9. 🌳 Показать дерево поиска")
        print("0. 🚪 Выход")
        print("-" * 50)

        choice = input("Выберите действие (0-9): ").strip()

        if choice == "1":
            if player.current_playlist:
                player.current_playlist.show_all_songs()
            else:
                print("❌ Нет текущего плейлиста")

        elif choice == "2":
            if player.current_playlist:
                player.current_playlist.play_current()
            else:
                print("❌ Нет текущего плейлиста")

        elif choice == "3":
            if player.current_playlist:
                player.current_playlist.next_song()
            else:
                print("❌ Нет текущего плейлиста")

        elif choice == "4":
            if player.current_playlist:
                player.current_playlist.prev_song()
            else:
                print("❌ Нет текущего плейлиста")

        elif choice == "5":
            title = input("Введите название песни для поиска: ").strip()
            if title:
                player.search_song(title)

        elif choice == "6":
            print("\nКритерии сортировки:")
            print("1. По названию")
            print("2. По исполнителю")
            print("3. По длительности")
            sort_choice = input("Выберите критерий (1-3): ").strip()

            if sort_choice == "1":
                player.sort_songs(by="title")
            elif sort_choice == "2":
                player.sort_songs(by="artist")
            elif sort_choice == "3":
                player.sort_songs(by="duration")
            else:
                print("❌ Неверный выбор")

        elif choice == "7":
            print("\n➕ Добавление новой песни:")
            title = input("Название песни: ").strip()
            artist = input("Исполнитель: ").strip()
            album = input("Альбом (можно пропустить): ").strip()
            duration = input("Длительность в секундах: ").strip()

            if title and artist and duration.isdigit():
                album = album if album else None
                new_song = Song(title, artist, album, int(duration))
                player.add_song_to_player(new_song)
                print("✅ Песня успешно добавлена!")
            else:
                print("❌ Неверные данные")

        elif choice == "8":
            player.show_player_info()

        elif choice == "9":
            print("\n🌳 Дерево поиска песен:")
            player.song_tree.display_tree()

        elif choice == "0":
            print("\n🎵 Спасибо за использование музыкального плеера!")
            print("До свидания! 👋")
            break

        else:
            print("❌ Неверный выбор. Попробуйте снова.")

        input("\nНажмите Enter чтобы продолжить...")


# 🚀 Запускаем интерактивное меню
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🎵 ЗАПУСК МУЗЫКАЛЬНОГО ПЛЕЕРА")
    print("=" * 50)

    # Спрашиваем, хотим ли запустить меню
    start = input("Запустить интерактивное меню? (да/нет): ").lower()

    if start in ["да", "д", "yes", "y"]:
        interactive_menu()
    else:
        print("\nПрограмма завершена. Вы можете запустить меню позже.")
        print("Для запуска меню вызовите функцию interactive_menu()")