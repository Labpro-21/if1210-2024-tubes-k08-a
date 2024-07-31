from utils.coroutines import *
from game.state import *
from os import path, makedirs

def _menu_show_save(state, args):
    if state is SuspendableInitial:
        gameState, console, currentDirectory = args
        return 1, gameState, console, currentDirectory
    if state == 1:
        gameState, console, currentDirectory = args
        print, input, meta = console
        meta(action="clear")
        print("=========== SAVE ===========")
        print("Silahkan masukkan nama save.")
        saveName = input(f"Save: ", f"Kosongkan untuk menggunakan folder save saat ini.")
        return 2, gameState, console, currentDirectory, saveName
    if state == 2:
        gameState, console, currentDirectory, saveName = args
        print, input, meta = console
        meta(action="clear")
        if saveName is None:
            return SuspendableReturn, False
        savePath = gameState["directory"] # This is illegal access
        if saveName != "":
            savePath = path.join(currentDirectory, saveName)
        if not path.exists(savePath) or not path.isdir(savePath):
            print(f"Membuat folder {savePath}...")
            makedirs(savePath)
        gamestate_change_save_dir(gameState, savePath)
        gamestate_save(gameState)
        print(f"Berhasil menyimpan data di folder {savePath}!")
        input("Lanjut", selectable=True)
        selection = meta(action="select")
        return 3, gameState, console, selection
    if state == 3:
        return SuspendableReturn, True
    return SuspendableExhausted
