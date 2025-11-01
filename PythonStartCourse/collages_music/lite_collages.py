# 🎵 Простой Музыкальный Коллаж 🖼️
import os
import random
from PIL import Image
import pygame

# Настройки
MUSIC_FOLDER = "music"
IMAGES_FOLDER = "images"
OUTPUT_FOLDER = "collages"


def setup_folders():
    """Создаем папки если их нет"""
    for folder in [MUSIC_FOLDER, IMAGES_FOLDER, OUTPUT_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Создана папка: {folder}")


def get_files(folder, extensions):
    """Получаем файлы с нужными расширениями"""
    files = []
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if any(file.lower().endswith(ext) for ext in extensions):
                files.append(file)
    return files


def play_random_music():
    """Играем случайную музыку"""
    music_files = get_files(MUSIC_FOLDER, ['.mp3', '.wav'])

    if not music_files:
        print("❌ Добавьте MP3 файлы в папку 'music'")
        return None

    random_music = random.choice(music_files)
    music_path = os.path.join(MUSIC_FOLDER, random_music)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        print(f"🎵 Играет: {random_music}")
        return random_music
    except:
        print("❌ Ошибка воспроизведения")
        return None


def create_simple_collage(music_name):
    """Создаем простой коллаж без текста"""
    image_files = get_files(IMAGES_FOLDER, ['.jpg', '.jpeg', '.png'])

    if not image_files:
        print("❌ Добавьте картинки в папку 'images'")
        return

    # Создаем холст
    collage = Image.new('RGB', (800, 600), 'black')

    # Берем до 4 случайных картинок
    selected_images = random.sample(image_files, min(4, len(image_files)))

    # Позиции для картинок
    positions = [(50, 50), (400, 50), (50, 300), (400, 300)]

    for i, img_name in enumerate(selected_images):
        if i >= 4:  # Максимум 4 картинки
            break

        try:
            img_path = os.path.join(IMAGES_FOLDER, img_name)
            img = Image.open(img_path)
            img = img.resize((300, 200))  # Уменьшаем размер

            # Размещаем на коллаже
            collage.paste(img, positions[i])

        except Exception as e:
            print(f"❌ Ошибка с {img_name}: {e}")

    # Сохраняем (без текста чтобы избежать ошибок с шрифтами)
    import time
    output_name = f"collage_{int(time.time())}.png"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    collage.save(output_path)

    print(f"🎨 Коллаж сохранен: {output_path}")
    print(f"🎵 Под музыку: {music_name}")
    return output_path


def show_info():
    """Показываем информацию о файлах"""
    music_count = len(get_files(MUSIC_FOLDER, ['.mp3', '.wav']))
    images_count = len(get_files(IMAGES_FOLDER, ['.jpg', '.jpeg', '.png']))
    collages_count = len(get_files(OUTPUT_FOLDER, ['.png']))

    print(f"\n📊 В папках:")
    print(f"🎵 Музыкальных файлов: {music_count}")
    print(f"🖼️ Изображений: {images_count}")
    print(f"🎨 Создано коллажей: {collages_count}")


def main():
    """Главная функция"""
    print("""
    🎵 ПРОСТОЙ МУЗЫКАЛЬНЫЙ КОЛЛАЖ 🖼️
    ================================
    """)

    setup_folders()

    while True:
        print("\n" + "=" * 40)
        print("1 - 🎵 Создать коллаж с музыкой")
        print("2 - 📊 Информация о файлах")
        print("3 - ❌ Остановить музыку")
        print("4 - 🚪 Выйти")

        choice = input("\nВыберите действие (1-4): ")

        if choice == '1':
            music = play_random_music()
            if music:
                create_simple_collage(music)

        elif choice == '2':
            show_info()

        elif choice == '3':
            try:
                pygame.mixer.music.stop()
                print("⏹️ Музыка остановлена")
            except:
                pass

        elif choice == '4':
            print("👋 До свидания!")
            break

        else:
            print("❌ Неверный выбор")


main()
