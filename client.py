import socket
import threading
from time import sleep

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname() # "127.0.1.1"
port = 8000

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

if msg == 'READY':
    print(f'{msg}')

status = my_socket.recv(1024).decode()

while status == 'NDONE':
    msg = my_socket.recv(1024).decode()
    print(msg)

    print('Loading ', end='', flush=True)

    for x in range(2):
        for frame in r'-\|/-\|/':

            print('\b', frame, sep='', end='', flush=True)
            sleep(0.2)

    print('\b ')

    guess = input('Enter a letter: ')
    my_socket.sendall(guess.encode('ascii'))
    status = my_socket.recv(1024).decode()
    if status == 'ERR':
        print(my_socket.recv(1024).decode())
    status = my_socket.recv(1024).decode()
