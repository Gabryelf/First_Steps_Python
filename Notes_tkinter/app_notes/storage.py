import json

FILE_NAME = "notes.json"


def save_notes(notes):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def load_notes():
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []