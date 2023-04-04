from multiprocessing import Process
# from threading import Thread
import socket
import hang
from random import randint

players = list()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = socket.gethostname()
PORT = 5001 
server.bind((ADDR, PORT))
server.listen(2)

def start():
    for player in players:
        player.conn.send("NDONE".encode())

    with open('movies.txt', 'r', errors='replace') as f:
        movList = f.readlines()
        key = movList[randint(0, len(movList))]

        t1 = Process(target=hang.game, args=(players[0], key[:-1], hang.makeMovie(key[:-1]), 1))
        t2 = Process(target=hang.game, args=(players[1], key[:-1], hang.makeMovie(key[:-1]), 2))

        t1.start()
        t2.start()

        while(t1.is_alive() and t2.is_alive()):
            continue

        if(players[0].won and players[1].won):
            print("Draw")
        elif(players[0].won and t2.is_alive()):
            print(f'{players[0].name}')
            t2.terminate()
        elif(players[1].won and t1.is_alive()):
            print(f'{players[1].name}')
            t1.terminate()



while True:
    conn, addr = server.accept()
    name = conn.recv(1024).decode()
    print(f'{name} has entered')
    players.append(hang.Player(name, conn, addr))
    if len(players) == 1:
        conn.send("WAITING".encode())
        continue
    else:
        conn.send("random".encode())
        for player in players:
            player.conn.send("READY".encode())

    break

start()

