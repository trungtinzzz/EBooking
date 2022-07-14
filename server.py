from dataclasses import dataclass
import socket
import json
import pickle
import datetime
import threading
HOST = '127.0.0.1'
PORT = 8003

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'


def sendimage(hotelname, dicthotel):
    for i in range(len(dicthotel)):
        f = open('data/'+hotelname+'/'+dicthotel[hotelname][i]['no']+'.jpg','rb')
        client.send(f.read())


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
    client.send(username.encode())
    password = client.recv(1024).decode()
    client.send(password.encode())

    for i in account_list:
        if username == i['username'] and password == i['password']:
            client.send('OK'.encode())
            return (True, username)
    client.send('Fail'.encode())
    return (False, '')


def signup(account_list):
    username = client.recv(1024).decode()
    client.send(username.encode())
    password = client.recv(1024).decode()
    client.send(password.encode())
    bankno = client.recv(1024).decode()
    client.send(bankno.encode())

    if not checkvalidacc(username, password, bankno):
        client.send('Fail'.encode())
        return False
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
            checkout = datetime.datetime.strptime(j['checkout'], '%Y-%m-%d')
            if checkout.date() > ans[1]:
                checkn = checkn + 1
        if checkn == 0:
            list_of_available_room.append(i)
    return list_of_available_room


def booking_menu(list_of_valid_room, ans, username):
    while True:
        sub_ans = client.recv(1024).decode()
        if sub_ans == '1':
            list_of_booked = client.recv(1024).decode()
            list_of_booked = eval(list_of_booked)
            cost = 0
            for i in list_of_valid_room:
                if i['no'] in list_of_booked:
                    cost = cost + i['price'] * ((ans[2] - ans[1]).days)
            client.send(str(cost).encode())
            order_data_str = client.recv(1024).decode()
            order_time = datetime.datetime.strptime(order_data_str, '%Y-%m-%d %H:%M:%S')
            code = str(order_time.year) + str(order_time.month) + str(order_time.day)
            code = code + str(order_time.hour) + str(order_time.minute) + str(order_time.second)
            f = open('data/order.json')
            order_dict = json.load(f)
            f.close()
            f = open('data/hoteldata.json')
            hotel_dict = json.load(f)
            f.close()
            list_of_no = list_of_booked[:len(list_of_booked) - 1]
            new_order = {
                "hotel": ans[0],
                "order_time": order_data_str,
                "no": list_of_no,
                "checkin": datetime.datetime.strftime(ans[1], '%Y-%m-%d'),
                "checkout": datetime.datetime.strftime(ans[2], '%Y-%m-%d')
            }
            order_dict[username][code] = new_order
            for i in hotel_dict[ans[0]]:
                if i['no'] in list_of_booked:
                    new_hot_order = {
                        "booker": username,
                        "order_time": order_data_str,
                        "checkin": datetime.datetime.strftime(ans[1], '%Y-%m-%d'),
                        "checkout": datetime.datetime.strftime(ans[2], '%Y-%m-%d')
                    }
                    i['booked'].append(new_hot_order)
            if len(list_of_no) > 0:
                with open('data/order.json', 'w') as f:
                    json.dump(order_dict, f, indent=4)
                with open('data/hoteldata.json', 'w') as f:
                    json.dump(hotel_dict, f, indent = 4)
            break
        else:
            break
        
def menu_listener(username):
    while True:
        ans = client.recv(1024).decode()
        if ans == '1':
            hotel_name = client.recv(1024).decode()
            f = open('data/hoteldata.json')
            hotel_dict = json.load(f)
            f.close()
            if hotel_name not in hotel_dict:
                client.send('Fail'.encode())
            else:
                client.send('OK'.encode())
                ans = client.recv(1024).decode()
                ans = eval(ans)
                list_of_available_room = search_for_room(hotel_dict, ans)
                client.send(str(list_of_available_room).encode())
                if len(list_of_available_room) > 0:
                    booking_menu(hotel_dict[ans[0]], ans, username)
        elif ans == '2':
            hotel_name = client.recv(1024).decode()
            f = open('data/order.json')
            order_dict = json.load(f)
            f.close()
            list_of_order = []
            for k, v in order_dict[username].items():
                if v['hotel'] == hotel_name:
                    list_of_order.append(k)
            client.send(str(list_of_order).encode())
            if len(list_of_order) > 0:
                code = client.recv(1024).decode()
                if code not in order_dict[username]:
                    client.send('Not found'.encode())
                else:
                    client.send('OK'.encode())
                    key = order_dict[username][code]['order_time']
                    key_time = datetime.datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
                    if (key_time - datetime.datetime.now()).total_seconds() < 24.0 * 3600:
                        client.send('OK'.encode())
                        order_dict[username].pop(code)
                        with open('data/order.json', 'w') as f:
                            json.dump(order_dict, f, indent = 4)
                        #delete in hoteldatajson
                        f = open('data/hoteldata.json')
                        hotel_dict = json.load(f)
                        f.close()
                        for i in hotel_dict[hotel_name]:
                            tmp_list = []
                            for j in i['booked']:
                                if j['order_time'] != key:
                                    tmp_list.append(j)
                            i['booked'] = tmp_list
                        with open('data/hoteldata.json', 'w') as f:
                            json.dump(hotel_dict, f, indent = 4)
                    else:
                        client.send('Fail'.encode())
        elif ans == '3':
            f = open('data/hoteldata.json')
            hotel_dict = json.load(f)
            f.close()
            keys = list(hotel_dict.keys())
            client.send(str(keys).encode())
        else:
            break


def handleClient(client, addr):
    file_of_account = open('data/account.json')
    raw_account_list = json.load(file_of_account)
    print('Connected by', addr)
    
    option = client.recv(1024).decode()
    count = 0
    while(count < 50):
        if option == 'LOGIN':
            username = ''
            check, username = login(raw_account_list)
            if check == True:
                menu_listener(username)
            option = 'X'
        elif option == 'SIGNUP':
            signup(raw_account_list)
            option = 'X'
        count += 1
    
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