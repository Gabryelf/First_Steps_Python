from User import User

users = [
    User('pass1', 'login1', 'User 1',),
    User('pass2', 'login2', 'User 2',),
    User('pass3', 'login3', 'User 3',),
]

user_repos = {user.get_login(): user for user in users}


def get_user_by_login(login):
    return user_repos.get(login)
