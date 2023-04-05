import socket
from threading import Thread
from time import sleep
import sys

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname() # "127.0.1.1"
port = 8001

try:
    my_socket.connect((host, port))
except:
    print("Server not up")
    exit()

nickname = input("Choose your name : ").strip()
while not nickname:
    nickname = input("Your name should not be empty : ").strip()

my_socket.sendall(nickname.encode())

msg = my_socket.recv(1024).decode()
if msg == 'WAITING':
    print('Waiting for another player...')

msg = my_socket.recv(1024).decode()

turn = ''

def listening():
    while True:
        global turn
        ques = my_socket.recv(1024).decode()
        if ques == "Your Turn\n":
            turn = ques
        elif ques == "Other Player's Turn\n":
            turn = ques
        elif ques == "DONE":
            my_socket.close()
            sys.exit(0)
        else:
            print("\n"+ques)

def sending():
    while True:
        l = input()
        if turn == "Other Player's Turn\n":
            print("\nNOT YOUR TURN")
            continue
        else:
            my_socket.sendall(l.encode())

t1 = Thread(target=listening)
t2 = Thread(target=sending)
t1.start()
t2.start()

