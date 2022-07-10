import socket

HOST = '127.0.0.1'
PORT = 8001


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

print('1.Log in \n 2.Sign up \n 3.Exit')
choose = input()
if choose == '1':
    sock.send('1'.encode())
    clogin()
elif choose == '2':
    sock.send('2'.encode())
    csignup()
elif choose == '3':
    sock.send('3'.encode())

sock.close()
