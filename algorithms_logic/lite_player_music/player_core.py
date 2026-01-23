from song_data import songs

# Текущая позиция
now_playing = 0
total = len(songs)


def show_song(n):
    if 0 <= n < total:
        m = songs[n][2] // 60
        s = songs[n][2] % 60
        return f"{songs[n][0]} - {songs[n][1]} [{m}:{s:02d}]"
    return "No song"


def next_song():
    global now_playing
    if now_playing < total - 1:
        now_playing += 1
    else:
        now_playing = 0
    return now_playing


def prev_song():
    global now_playing
    if now_playing > 0:
        now_playing -= 1
    else:
        now_playing = total - 1
    return now_playing


def find_songs(text):
    results = []
    text = text.lower()
    for i, song in enumerate(songs):
        if text in song[0].lower() or text in song[1].lower():
            results.append(i)
    return results


def sort_by(what):
    global songs, now_playing
    if what == "name":
        songs.sort(key=lambda x: x[0].lower())
    elif what == "artist":
        songs.sort(key=lambda x: x[1].lower())
    elif what == "time":
        songs.sort(key=lambda x: x[2])
    # Находим новую позицию текущей песни
    for i, song in enumerate(songs):
        if song[0] == songs[now_playing][0]:
            now_playing = i
            break


def add_song(name, artist, seconds):
    global songs, total
    songs.append([name, artist, seconds])
    total = len(songs)
    return True


def stats():
    if not songs:
        return 0, 0, 0

    total_time = sum(s[2] for s in songs)
    avg_time = total_time // total

    longest = max(songs, key=lambda x: x[2])
    shortest = min(songs, key=lambda x: x[2])

    return total_time, avg_time, longest, shortest


