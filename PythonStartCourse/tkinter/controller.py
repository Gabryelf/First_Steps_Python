import user_repository


def auth_user(login, password):
    user = user_repository.get_user_by_login(login.strip())
    massage: str = "Доступ запрещен"
    if user is None:
        pass
    else:
        if user.check_password(password.strip()):
            massage = f"ПРИВЕТ - {user.get_name()}"
        print(massage)
