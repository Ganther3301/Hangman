from multiprocessing import Process
# from threading import Thread
import socket
import hang
from time import sleep
from random import randint

players = list()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = socket.gethostname()
PORT = 8001 
server.bind((ADDR, PORT))
server.listen()

def start():
    while True:
        score = 0 
        for player in players:
            if player.turn == False:
                player.conn.sendall("False".encode())
                player.conn.sendall("Enter movie name: ".encode())
                key = player.conn.recv(1024).decode()
                key = key+'a'
            else:
                player.conn.sendall("True".encode())
                score = player.score

        hang.game(players, key[:-1], hang.makeMovie(key[:-1]))

        if players[0].turn == True:
            if players[0].score > score:
                for player in players:
                    player.conn.sendall(f"{players[0].name} got a point".encode())
            else:
                for player in players:
                    player.conn.sendall(f"{players[0].name} didn't get a point".encode())
                    player.conn.sendall(f"Answer is {key[:-1]}".encode())
            players[0].turn = False
            players[1].turn = True

        elif players[1].turn == True:
            if players[1].score > score:
                for player in players:
                    player.conn.sendall(f"{players[1].name} got a point".encode())

            else:
                for player in players:
                    player.conn.sendall(f"{players[1].name} didn't get a point".encode())
                    player.conn.sendall(f"Answer is {key[:-1]}".encode())

            players[1].turn = False
            players[0].turn = True

        sleep(5)




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

players[0].turn = True

start()