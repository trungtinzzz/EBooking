from operator import is_
import socket
import json
import threading
HOST = '127.0.0.1'
PORT = 8000


def login(account_list):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    for i in account_list:
        if username == i['username'] and password == i['password']:
            client.send('Login successfully'.encode())
            return True
    client.send('Login fail'.encode())
    return False


def signup(account_list):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    bankno = client.recv(1024).decode()
    for i in account_list:
        if username == i['username']:
            client.send('Sign up fail'.encode())
            return False
    newuser = {'username': username, 'password': password, 'bank account number': bankno}
    account_list.append(newuser)
    f = open('data/account.json', 'w')
    json_object = json.dumps(account_list, indent=4)
    f.write(json_object)
    f.close()
    client.send('Sign up successfully'.encode())
    return True

def handleClient(client, addr):
    file_of_account = open('account.json')
    raw_account_list = json.load(file_of_account)
    file_of_account.close()
    print('Connected by', addr)
    is_off = False
    while not is_off:
        choose = client.recv(1024).decode()
        if choose == '0':
            is_off = True
        elif choose == '1':
            login(raw_account_list)
        elif choose == '2':
            signup(raw_account_list)
    print("Client", addr, "finished")
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
