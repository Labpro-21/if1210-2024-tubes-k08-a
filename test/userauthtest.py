from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from game.database import *
from testutils import Formatter
from os import path

if __name__ == "__main__":
    currentDirectory = path.dirname(__file__)
    savesDirectory = path.join(currentDirectory, "../data/saves/test-save/")
    gameState = gamestate_new(savesDirectory)
    # gamestate_save(gameState)

    import game.user as u
    while True:
        print("Select test action")
        print("1. Check if logged in")
        print("2. Register user")
        print("3. Login user")
        print("4. logout user")
        print("5. Inspect user database")
        print("6. exit")
        choice = int(input())
        if choice == 1:
            print("Is logged in: " + str(u.user_is_logged_in(gameState)))
        if choice == 2:
            u.user_register(gameState)
        if choice == 3:
            u.user_login(gameState)
        if choice == 4:
            u.user_logout(gameState)
        if choice == 5:
            userDatabase = gamestate_get_user_database(gameState)
            print(Formatter()(userDatabase))
        if choice == 6:
            exit()
        print("\n\n")

    # looper = looper_new("Main")
    # with looper_closure(looper):
    #     set_interval(loop, 15)
    # while True:
    #     looper_tick(looper)
