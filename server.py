import socket
import json
import pickle
import datetime

HOST = '127.0.0.1'
PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)
print('Waiting for connection......')
client, addr = sock.accept()

def login(account_list):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    for i in account_list:
        if username == i['username'] and password == i['password']:
            client.send('OK'.encode())
            return True
    client.send('Fail'.encode())
    return False


def signup(account_list):
    username = client.recv(1024).decode()
    password = client.recv(1024).decode()
    bankno = client.recv(1024).decode()
    for i in account_list:
        if username == i['username']:
            client.send('Fail'.encode())
            return False
    newuser = {'username': username, 'password': password, 'bank account number': bankno}
    account_list.append(newuser)
    f = open('data/account.json', 'w')
    json_object = json.dumps(account_list, indent=4)
    f.write(json_object)
    f.close()
    client.send('OK'.encode())
    return True

def search_for_room(dict_of_hotel, ans):
    print(ans[0])
    list_of_available_room = []
    for i in dict_of_hotel[ans[0]]:
        checkn = 0
        for j in i['booked']:
            if j['out_year'] > ans[1].year:
                checkn = checkn + 1
            elif j['out_year'] == ans[1].year:
                if j['out_month'] > ans[1].month:
                    checkn = checkn + 1
                elif j['out_month'] == ans[1].month:
                    if j['out_date'] >= ans[1].date:
                        checkn = checkn + 1
        if checkn == 0:
            list_of_available_room.append(i)
    return list_of_available_room
    

def menu_listener():
    while True:
        ans = client.recv(1024).decode()
        if ans == '1':
            ans = client.recv(1024).decode()
            ans = eval(ans)
            file_of_hotel = open('data/hoteldata.json')
            dict_of_hot = json.load(file_of_hotel)
            file_of_hotel.close()
            if ans[0] in dict_of_hot:
                client.send('OK'.encode())

                list_of_available_room = search_for_room(dict_of_hot, ans)
                client.send(str(list_of_available_room).encode())
            else:
                client.send('Fail'.encode())
        else:
            break

def init_listener():
    choose = client.recv(1024).decode()
    if choose == '1':
        check = login(raw_account_list)
        if check == True:
            menu_listener()
    elif choose == '2':
        signup(raw_account_list)



file_of_account = open('data/account.json')
raw_account_list = json.load(file_of_account)
file_of_account.close()
print('Connected by', addr)
init_listener()
    
sock.close()
