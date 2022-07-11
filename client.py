import socket

HOST = '127.0.0.1'
PORT = 8000


def clogin():
    print('Username:')
    sock.send(input().encode())
    print('Password:')
    sock.send(input().encode())
    print(sock.recv(1024).decode())


def csignup():
    print('Username:')
    sock.send(input().encode())
    print('Password:')
    sock.send(input().encode())
    print('Bank account number:')
    sock.send(input().encode())
    print(sock.recv(1024).decode())


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('You are connecting to', HOST, PORT)
sock.connect((HOST, PORT))

is_off = False
while not is_off:
    #Menu
    choices = ['0. Exit', '1. Login', '2. Sign up']
    for i in choices:
        print(i)
    choose = input()
    if choose == '0':
        sock.send('0'.encode())
        is_off = True
    elif choose == '1':
        sock.send('1'.encode())
        clogin()
    elif choose == '2':
        sock.send('2'.encode())
        csignup()

sock.close()
