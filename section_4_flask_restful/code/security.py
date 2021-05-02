from user import User
from werkzeug.security import safe_str_cmp

listUser = [
    User(1, 'Bob', 'asdf')
]

username_mapping = {u.username: u for u in listUser}

userid_mapping = {u.id: u for u in listUser}

def authentication(username, password):
    print(username)
    print(password)
    user: User = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
