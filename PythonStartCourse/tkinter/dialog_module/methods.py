import os


class Methods:
    @staticmethod
    def get_note_list():
        return [file for file in os.listdir() if file.endswith('.note')]
