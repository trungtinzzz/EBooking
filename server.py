import socket

HOST = '127.0.0.1'
PORT = 8000


def login(username, password):
    try:
        client.send('Username'.encode())
        clientusername = client.recv(1024).decode()
        client.send('Password'.encode())
        clientpassword = client.recv(1024).decode()
        if clientusername == username and clientpassword == password:
            client.send('Login successful'.encode())
            return True
        else:
            client.send('Login fail'.encode())
            return False
    finally:
        client.close()


def signup(acclist):
    client.send('Username'.encode())
    username = client.recv(1024).decode()
    client.send('Password'.encode())
    password = client.recv(1024).decode()
    for i in acclist:
        if username == list[i][0]:
            client.send('Sign up fail'.encode())
            return False
    acclist.append(username, password)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)
client, addr = sock.accept()
print('Connected by', addr)
login('luan', '1234')
