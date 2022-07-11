import socket
import json
HOST = '127.0.0.1'
PORT = 8000


def login(dictacc):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    for i in dictacc:
        if username == i['username'] and password == i['password']:
            client.send('Login successfully'.encode())
            return True
    client.send('Login fail'.encode())
    return False


def signup(dictacc):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    bankno = client.recv(1024).decode()
    for i in dictacc:
        if username == i['username']:
            client.send('Sign up fail'.encode())
            return False
    newuser = {'username': username, 'password': password, 'bank account number': bankno}
    dictacc.append(newuser)
    f = open('account.json', 'w')
    json_object = json.dumps(dictacc, indent=4)
    f.write(json_object)
    client.send('Sign up successfully'.encode())
    return True


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)
print('Waiting for connection......')
client, addr = sock.accept()

fileacc = open('account.json')
dataacc = json.load(fileacc)
print('Connected by', addr)

choose = client.recv(1024).decode()
if choose == '1':
    login(dataacc)
if choose == '2':
    signup(dataacc)

sock.close()
