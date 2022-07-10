import socket

HOST = '127.0.0.1'
PORT = 8001


def login(listacc):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    for i in range(len(listacc[0])):
        if username == listacc[0][i]:
            if password == listacc[1][i]:
                client.send('Login successfully'.encode())
                return True
    client.send('Login fail'.encode())
    return False


def signup(listacc):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    bankno = client.recv(1024).decode()
    for i in range(len(listacc)):
        if username == listacc[0][i]:
            client.send('Sign up fail'.encode())
            return False
    listacc[0].append(username)
    listacc[1].append(password)
    listacc[2].append(bankno)
    client.send('Sign up successfully'.encode())
    return True


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print('Waiting for connection......')
client, addr = sock.accept()

listt = [['luan', 'tin', 'phuc'], ['123', '123', '123'], ['0123456789', '0123456789', '0123456789']]
print('Connected by', addr)
choose = client.recv(1024).decode()
if choose == '1':
    login(listt)
if choose == '2':
    signup(listt)

sock.close()
