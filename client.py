import socket

HOST = '127.0.0.1'
PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('connecting to', HOST, PORT)
sock.connect((HOST, PORT))

try:
    print(sock.recv(1024).decode())
    sock.send(input().encode())
    print(sock.recv(1024).decode())
    sock.send(input().encode())
    print(sock.recv(1024).decode())

finally:
    sock.close()
