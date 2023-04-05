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
    for i in range(3):
        score = 0 
        for player in players:
            if player.turn == False:
                player.conn.sendall("Other Player's Turn\n".encode())
                player.conn.sendall("Enter movie name: ".encode())
                key = player.conn.recv(1024).decode()
                key = key+'a'
            else:
                player.conn.sendall("Your Turn\n".encode())
                score = player.score

        hang.game(players, key[:-1], hang.makeMovie(key[:-1]))

        if players[0].turn == True:
            if players[0].score > score:
                for player in players:
                    player.conn.sendall(f"{players[0].name} got a point\n".encode())
            else:
                for player in players:
                    player.conn.sendall(f"{players[0].name} didn't get a point\n".encode())
                    player.conn.sendall(f"Answer is {key[:-1]}\n".encode())
            players[0].turn = False
            players[1].turn = True

        elif players[1].turn == True:
            if players[1].score > score:
                for player in players:
                    player.conn.sendall(f"{players[1].name} got a point\n".encode())

            else:
                for player in players:
                    player.conn.sendall(f"{players[1].name} didn't get a point\n".encode())
                    player.conn.sendall(f"Answer is {key[:-1]}\n".encode())

            players[1].turn = False
            players[0].turn = True

        for player in players:
            player.reset()

        sleep(2)

    if players[0].score > players[1].score:
        for player in players:
            player.conn.sendall(f'{players[0].name} has won with {players[0].score} points'.encode())
    elif players[1].score > players[0].score:
        for player in players:
            player.conn.sendall(f'{players[1].name} has won with {players[1].score} points'.encode())
    elif players[1].score == players[0].score:
        for player in players:
            player.conn.sendall("It's a draw".encode())

    for player in players:
        player.conn.sendall("DONE".encode())
    server.close()

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