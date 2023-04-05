from random import randint
from time import sleep
from threading import Thread

x = True
guess = ''

class Player:
    def __init__(self, name, conn, addr):
        # self.score = 0
        self.won = False
        self.hangman = "H A N G M A N"
        self.used = list()
        self.conn = conn
        self.name = name
        self.addr = addr

    def redHang(self):
        self.hangman = self.hangman[1:].lstrip()
    
    def check(self, key, letter, value):
        changed = False
        key = list(key)
        value = list(value)

        for k in range(len(key)):
            if letter == key[k]:
                value[k] = letter
                changed = True

        if not changed:
            self.redHang()

        return ''.join(key), ''.join(value)
    
    def isValid(self, guess):
        if len(guess) > 1:
            self.conn.sendall("ERR".encode())
            self.conn.sendall("\nENTER A SINGLE LETTER DUMB BITCH\n".encode())

            return 0

        if not guess.isalpha():
            self.conn.sendall("ERR".encode())
            self.conn.sendall("\nENTER A LETTER DUMB BITCH\n".encode())

            return 0

        if guess in self.used:
            self.conn.sendall("ERR".encode())
            self.conn.sendall("\nYOU'VE ALREADY USED THIS LETTER DUMB BITCH\n".encode())

            return 0
         
        self.conn.sendall("OK".encode())
        return 1
    
    def reset(self):
        self.used = list()
        self.hangman = "H A N G M A N"

def makeMovie(movie):
    res = ""

    for m in movie:
        if m.isalpha():
            res += "_"
        
        else:
            res += m

    return res

# def listening(player):
#     while True:
#         global guess
#         guess = player.conn.recv(1024).decode()
#         print(guess)
#         global x
#         x = False

def game(player, key, value, t):
    # t1 = Thread(target=listening, args=(player,))
    gameFlag = True
    retMsg = ""
    # t1.start()

    while(gameFlag):
        # player.conn.sendall(f"\nUsed - {' '.join(player.used)}\n".encode())
        # player.conn.sendall(f"{value}\n".encode())
        # player.conn.sendall(f"{player.hangman}\n".encode())
        # player.conn.sendall("HEHE".encode())

        ques = f"\nUsed - {' '.join(player.used)}\n{value}\n{player.hangman}\n"
        player.conn.sendall(ques.encode())
        guess = player.conn.recv(1024).decode()
        print(guess)

        # guess = input("Enter a letter: ").lower()
        # sleep(t)
        # global x
        # while(x):
        #     continue
        # x = True

        # guess = player.conn.recv(1024).decode()

        if(not player.isValid(guess)):
            player.conn.sendall("NDONE".encode()) 
            continue

        player.used.append(guess)

        key, value = player.check(key, guess, value)

        if(key == value):
            player.won = True
            gameFlag = False
            player.conn.sendall("DONE".encode()) 
            continue

        if(not len(player.hangman) > 0):
            gameFlag = False
            player.conn.sendall("DONE".encode()) 
            continue

        player.conn.sendall("NDONE".encode()) 



if __name__ == '__main__':
    player_1 = Player()

    flag = True

    while(flag):
        choice = input("Enter -\n1 to play HANGMAN\n2 to quit\n")

        if(choice == '1'):
            with open('movies.txt', 'r', errors='replace') as f:
                movList = f.readlines()
                key = movList[randint(0, len(movList))]

            msg = game(player_1, key[:-1], makeMovie(key[:-1]))
            print(msg)
            player_1.reset()

            continue

        if(choice == '2'):
            print("\nThank you for playing HANGMAN!!\n")
            flag = False

    
