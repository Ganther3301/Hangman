from multiprocessing import Process
# from threading import Thread
import socket
import hang
from random import randint

players = list()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = socket.gethostname()
PORT = 8000 
server.bind((ADDR, PORT))
server.listen()

def start():
    for player in players:
        player.conn.send("NDONE".encode())

    with open('movies.txt', 'r', errors='replace') as f:
        movList = f.readlines()
        key = movList[randint(0, len(movList))]
        key = 'john wickk'

        t1 = Process(target=hang.game, args=(players[0], key[:-1], hang.makeMovie(key[:-1]), 1))
        t2 = Process(target=hang.game, args=(players[1], key[:-1], hang.makeMovie(key[:-1]), 2))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        while(t1.is_alive() and t2.is_alive()):
            continue

        if(players[0].won ==False and players[1].won == False):
            t1.terminate()
            t2.terminate()
        elif(players[0].won and t2.is_alive()):
            players[0].conn("win".encode())
            t2.terminate()
        elif(players[1].won and t1.is_alive()):
            players[1].conn("win".encode())
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

