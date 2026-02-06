class User:
    def __init__(self, password, login, fio):
        self._password = password
        self._login = login
        self._fio = fio

    def check_password(self, pass_word):
        return self._password == pass_word

    def get_name(self):
        return self._fio

    def get_login(self):
        return self._login
