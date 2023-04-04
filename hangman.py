import os
from random import *
from time import *


turn = 0


players = {
    0: {
        "name": "Player 1",
        "score": 0
    },

    1: {
        "name": "Player 2",
        "score": 0
    }
}

def makeMovie(movie):
    res = ""

    for m in movie:
        if m.isalpha():
            res += "_"
        
        else:
            res += m

    return res

def redHang(hangman):
    hangman = hangman[1:].lstrip()

    return hangman

def check(key, letter, value, hangman):
    changed = False
    key = list(key)
    value = list(value)

    for k in range(len(key)):
        if letter == key[k]:
            value[k] = letter
            changed = True

    if not changed:
        hangman = redHang(hangman)

    return ''.join(key), ''.join(value), hangman

def game(turn, key, value, hangman):
    gameFlag = True
    retMsg = ""
    used = []

    while(gameFlag):
        print(f"\nUsed - {' '.join(used)}\n")
        print(f"{value}\n")
        print(f"{hangman}\n")

        guess = input("Enter a letter: ").lower()

        if len(guess) > 1:
            print("\nENTER A SINGLE LETTER DUMB BITCH\n")
            sleep(3)
            continue

        if not guess.isalpha():
            print("\nENTER A LETTER DUMB BITCH\n")
            sleep(3)
            continue

        if guess in used:
            print("\nYOU'VE ALREADY USED THIS LETTER DUMB BITCH\n")
            sleep(3)
            continue

        used.append(guess)

        key, value, hangman = check(key, guess, value, hangman)

        if(key == value):
            os.system('cls')
            retMsg = "YOU WIN!\n\n\n"
            gameFlag = False

        if(not len(hangman) > 0):
            os.system('cls')
            retMsg = f"YOU LOSE! The word was {key.upper()}\n\n\n"
            gameFlag = False

    return retMsg


if __name__ == '__main__':
    hangman = "H A N G M A N"

    flag = True

    while(flag):
        choice = input("Enter -\n1 to play HANGMAN\n2 to quit\n")

        if(choice == '1'):
            with open('movies.txt', 'r', errors='replace') as f:
                movList = f.readlines()
                key = movList[randint(0, len(movList))]

            msg = game(0, key[:-1], makeMovie(key[:-1]), hangman)
            print(msg)

            continue

        if(choice == '2'):
            print("\nThank you for playing HANGMAN!!\n")
            flag = False

    
