from utils.primordials import *
from utils.coroutines import *
from utils.console import *
from game.state import *
from os import path

def loop():
    pass

if __name__ == "__main__":
    currentDirectory = path.dirname(__file__)
    savesDirectory = path.join(currentDirectory, "./data/saves/test-save/")
    gameState = gamestate_new(savesDirectory)
    # gamestate_save(gameState)

    import game.user as u
    print(u.user_is_exists(gameState, "Mr_Monogram"))

    # looper = looper_new("Main")
    # with looper_closure(looper):
    #     set_interval(loop, 15)
    # while True:
    #     looper_tick(looper)
