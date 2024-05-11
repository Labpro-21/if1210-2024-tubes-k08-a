# Convention

Only expose public functions. Do not expose internal functions if you think that function does not relate directly to the module, or if that function might have side effects, or perhaps that function could broke something else if used without responsibility. This also applies to variables.

For example, do not expose function `_user_hash_password` in `user/user.py`, because it might expose to security vulnerabilities, as the attacker somehow could import it from another module and could figure out what hashing algorithm is used. This is a bit of an extreme example, but you should get the idea.

The convention I decided to use in this projects:
1. In implementation file (in this case, `user/user.py`), you must name your variable starting with "_" (underscore). This is important because, by default, python does not export variable starting with underscore. This ensures that you need to explicitly write the function name in `__init__.py`.
2. In `__init__.py` you need to import the variables/functions from user.py, then re-export it by redeclaring another variable. The redeclared variable name is simply the original variables/functions name without the leading leading (beginning) underscore.

See this example to understand more:

- `user/user.py`
```python
# Do NOT expose this function in __init__.py.
def _user_hash_password(password: str):
    pass

def _user_is_logged_in(gameState: GameState):
    pass

def _user_is_exists(gameState: GameState):
    pass

def _user_register(gameState: GameState):
    pass

def _user_login(gameState: GameState):
    pass

def _user_logout(gameState: GameState):
    pass
```

- `user/__init__.py`
```py
# Note: You do need the dot before the module name. This means to use import with relative path.
from .user import _user_is_logged_in, _user_is_exists, _user_register, _user_login, _user_logout

user_is_logged_in = _user_is_logged_in
user_is_exists = _user_is_exists
user_register = _user_register
user_login = _user_login
user_logout = _user_logout
```
