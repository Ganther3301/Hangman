import socket
import threading

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname() # "127.0.1.1"
port = 5001

try:
    my_socket.connect((host, port))
except:
    print("Server not up")
    exit()

nickname = input("Choose your name : ").strip()
while not nickname:
    nickname = input("Your name should not be empty : ").strip()

my_socket.send(nickname.encode())

msg = my_socket.recv(1024).decode()
if msg == 'WAITING':
    print('Waiting for another player...')

msg = my_socket.recv(1024).decode()

if msg == 'READY':
    print(f'{msg}')

status = my_socket.recv(1024).decode()

while status == 'NDONE':
    for i in range(2):
        print(my_socket.recv(1024).decode())

    guess = input('Enter a letter: ').lower()
    my_socket.send(guess.encode())
    status = my_socket.recv(1024).decode()
    if status == 'ERR':
        print(my_socket.recv(1024).decode())
    status = my_socket.recv(1024).decode()
