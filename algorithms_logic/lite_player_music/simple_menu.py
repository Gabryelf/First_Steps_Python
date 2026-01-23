from player_core import *


def show_all():
    print("\n📀 Все песни:")
    for i in range(total):
        mark = "▶️ " if i == now_playing else "   "
        print(f"{mark}{i + 1}. {show_song(i)}")


def main():
    while True:
        print("\n" + "=" * 40)
        print(f"🎶 Сейчас: {show_song(now_playing)}")
        print(f"📊 {now_playing + 1}/{total}")
        print("=" * 40)

        print("1. ➡️  Следующая")
        print("2. ⬅️  Предыдущая")
        print("3. 📋 Все песни")
        print("4. 🔍 Поиск")
        print("5. 📊 Сортировка")
        print("6. ➕ Добавить")
        print("7. 📈 Статистика")
        print("0. 🚪 Выход")

        choice = input("\nВаш выбор: ")

        if choice == "1":
            next_song()

        elif choice == "2":
            prev_song()

        elif choice == "3":
            show_all()

        elif choice == "4":
            word = input("Что ищем: ")
            found = find_songs(word)
            if found:
                print(f"Найдено {len(found)}:")
                for idx in found:
                    print(f"  {idx + 1}. {show_song(idx)}")
            else:
                print("Не найдено")

        elif choice == "5":
            print("\nСортировать по:")
            print("1. Названию")
            print("2. Исполнителю")
            print("3. Времени")
            sort_choice = input("Выбор: ")
            if sort_choice == "1":
                sort_by("name")
            elif sort_choice == "2":
                sort_by("artist")
            elif sort_choice == "3":
                sort_by("time")

        elif choice == "6":
            name = input("Название: ")
            artist = input("Исполнитель: ")
            try:
                time = int(input("Секунды: "))
                add_song(name, artist, time)
                print("✅ Добавлено!")
            except:
                print("❌ Ошибка!")

        elif choice == "7":
            total_t, avg_t, longest, shortest = stats()
            print(f"\nВсего песен: {total}")
            print(f"Общее время: {total_t // 60}:{total_t % 60:02d}")
            print(f"Среднее: {avg_t} сек")
            print(f"Самая длинная: {longest[0]} ({longest[2]} сек)")
            print(f"Самая короткая: {shortest[0]} ({shortest[2]} сек)")

        elif choice == "0":
            print("\nПока! 🎵")
            break

        else:
            print("Неверный выбор")