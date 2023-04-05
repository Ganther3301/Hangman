import socket
from threading import Thread
from time import sleep

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
        if ques == "True":
            turn = ques
        elif ques == "False":
            turn = ques
        else:
            print("\n"+ques+"\n")

def sending():
    while True:
        l = input()
        if turn == 'False':
            print("\nNOT YOUR TURN\n")
            continue
        else:
            my_socket.sendall(l.encode())

t1 = Thread(target=listening)
t2 = Thread(target=sending)
t1.start()
t2.start()
