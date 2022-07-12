import socket
import json
import threading
HOST = '127.0.0.1'
PORT = 8000
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'


def checkvalidacc(username, password, bankno):
    if len(username) < 5:
        return False
    for i in username:
        if i not in LETTERS and i not in NUMBERS:
            return False
    if len(password) < 3:
        return False
    if len(bankno) != 10:
        return False
    for i in bankno:
        if i not in NUMBERS:
            return False
    return True


def login(account_list):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    for i in account_list:
        if username == i['username'] and password == i['password']:
            client.send('1'.encode())
            return True
    client.send('0'.encode())
    return False


def signup(account_list):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    bankno = client.recv(1024).decode()
    if not checkvalidacc(username, password, bankno):
        client.send('0'.encode())
        return False
    for i in account_list:
        if username == i['username']:
            client.send('0'.encode())
            return False
    newuser = {'username': username, 'password': password, 'bank account number': bankno}
    account_list.append(newuser)
    f = open('data/account.json', 'w')
    json_object = json.dumps(account_list, indent=4)
    f.write(json_object)
    client.send('1'.encode())
    f.close()
    return True

def handleClient(client, addr):
    file_of_account = open('account.json')
    raw_account_list = json.load(file_of_account)
    print('Connected by', addr)
    choose = client.recv(1024).decode()
    if choose == '1':
        while not login(raw_account_list):
            login(raw_account_list)
    if choose == '2':
        while not signup(raw_account_list):
            signup(raw_account_list)
    print("Client", addr, "finished")
    file_of_account.close()
    client.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)
print('Waiting for connection......')

nClient = 0
#allow up to 50 clients access
while(nClient < 50):
    client, addr = sock.accept()

    thr = threading.Thread(target=handleClient, args=(client,addr))
    thr.daemon = False
    thr.start()

    nClient += 1

sock.close()
