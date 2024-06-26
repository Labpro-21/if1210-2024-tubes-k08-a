input1 = str(input())
def exit():
    if input1 == "exit":
        print("Apakah Anda mau melakukan penyimpanan file yang sudah diubah? (y/n)")
        A = str(input())
        if A == "y":
            SystemExit()
        elif A == "Y":       
            SystemExit()
        elif A == "n":
            SystemExit()
        elif A == "N":
            SystemExit()
        else:
            exit()