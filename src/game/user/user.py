from utils.primordials import *
from game.state import *
from game.database import *

def _user_is_logged_in(gameState: GameState) -> bool:
    return gamestate_get_user_id(gameState) is not None

def _user_is_exists(gameState: GameState, username: str) -> bool:
    userDatabase = gamestate_get_user_database(gameState)
    for user in database_get_entries(userDatabase):
        if user.username != username:
            continue
        return True
    return False
    # Alternatively you could use: 
    # array_some(database_get_entries(userDatabase), lambda x: x.username == username)

def _user_register(gameState: GameState):
    userDatabase = gamestate_get_user_database(gameState)
    database_set_entry_at(userDatabase, 0, UserSchemaType(
        id=0,
        username="test",
        password="oioi",
        role="admin",
        money=10.2
    ))
    return

def _user_login(gameState: GameState):
    pass

def _user_logout(gameState: GameState):
    pass
