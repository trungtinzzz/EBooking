import socket
import json
import pickle
import datetime

HOST = '127.0.0.1'
PORT = 8003

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
            return (True, username)
    client.send('Fail'.encode())
    return (False, '')


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
            new_list = []
            if username in order_dict:
                new_list = order_dict[username]
            new_list.append(new_order)
            order_dict[username] = new_list
            for i in hotel_dict[ans[0]]:
                if i['no'] in list_of_booked:
                    new_hot_order = {
                        "booker": username, 
                        "checkin": datetime.datetime.strftime(ans[1], '%Y-%m-%d'),
                        "checkout": datetime.datetime.strftime(ans[2], '%Y-%m-%d')
                    }
                    i['booked'].append(new_hot_order)
            if len(list_of_no) > 0:
                with open('data/order.json', 'w') as f:
                    json.dump(order_dict, f)
                with open('data/hoteldata.json', 'w') as f:
                    json.dump(hotel_dict, f)
            break
        else:
            break
        
def menu_listener(username):
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
                booking_menu(dict_of_hot[ans[0]], ans, username)
            else:
                client.send('Fail'.encode())
        else:
            break
        
def init_listener():
    choose = client.recv(1024).decode()
    if choose == '1':
        username = ''
        check, username = login(raw_account_list)
        if check == True:
            menu_listener(username)
    elif choose == '2':
        signup(raw_account_list)



file_of_account = open('data/account.json')
raw_account_list = json.load(file_of_account)
file_of_account.close()
print('Connected by', addr)
init_listener()
    
sock.close()
