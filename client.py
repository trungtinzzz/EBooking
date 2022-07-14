from secrets import choice
import socket
import datetime
import pickle

HOST = '127.0.0.1'
PORT = 8003

def recvimage(hotelname, dicthotel):
    root = Tk()
    imagelist =[]
    for i in range(len(dicthotel)):
        f = open('client/'+str(i)+'.jpg', 'wb')
        data = sock.recv(1000000)
        f.write(data)
        imagelist.append(ImageTk.PhotoImage(Image.open('client/'+str(i)+'.jpg')))
        Label(image=imagelist[i]).grid(row=0,column=i)
        Label(text=dicthotel[hotelname][i]['no']).grid(row=1,column=i)
    root.mainloop()

    
def booking_menu(list_of_no):
    while True:
        booking_choices = ['0. Search for other hotels', '1. Booking']
        for i in booking_choices:
            print(i)
        b_choices = input('Your choice: ')
        sock.send(b_choices.encode())
        if b_choices == '1':
            print('Enter 0 to stop')
            list_of_booking = []
            booking_choice = input('No. of rooms: ')
            if booking_choice != '0' and booking_choice in list_of_no:
                list_of_booking.append(booking_choice)
                while booking_choice != '0' and booking_choice in list_of_no:
                    booking_choice = input('No. of rooms: ')
                    list_of_booking.append(booking_choice)
            sock.send(str(list_of_booking).encode())
            ans = eval(sock.recv(1024).decode())
            print('Booking successfully')
            print('Total cost:', ans)
            datetime_data = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            sock.send(datetime_data.encode())
            break
        else:
            break
        
def menu(username):
    while True:
        menu_choices = ['0. Exit', '1. Search for room', '2. List of order made', '3. List of hotels']
        for i in menu_choices:
            print(i)
        m_choices = input('Your choice: ')
        sock.send(m_choices.encode())
        if m_choices == '1':
            ans = input('Hotel name: ')
            sock.send(ans.encode())
            rep = sock.recv(1024).decode()
            if rep == 'Fail':
                print('Not found')
            else:
                print('Check in time: ')
                while True:
                    t_year = int(input('Year: '))
                    t_month = int(input('Month: '))
                    t_date = int(input('Date: '))
                    t_time_checkin = datetime.date(t_year, t_month, t_date)
                    if t_time_checkin < datetime.date.today():
                        print('Check in date invalid')
                    else:
                        break
                print('Check out time: ') 
                while True:
                    t_year = int(input('Year: '))
                    t_month = int(input('Month: '))
                    t_date = int(input('Date: '))
                    t_time_checkout = datetime.date(t_year, t_month, t_date)
                    if t_time_checkin > t_time_checkout:
                        print('Check out time invalid')
                    else:
                        break
                info = (ans, t_time_checkin, t_time_checkout)
                data_info = str(info)
                sock.send(data_info.encode())
                list_of_room = sock.recv(1024).decode()
                list_hot = eval(list_of_room)
                if len(list_hot) > 0:
                    list_of_no = []
                    for i in list_hot:
                        print('No.:' , i['no'])
                        print('Number of bed:', i['kind'])
                        print('Description:', i['des'])
                        print('Price:', i['price'], 'dollar a night')
                        list_of_no.append(i['no'])
                    print("-"*20)
                    booking_menu(list_of_no)
                else:
                    print('No room available')
        elif m_choices == '2':
            ans = input('Hotel name: ')
            sock.send(ans.encode())
            list_of_order = eval(sock.recv(1024).decode())
            if len(list_of_order) == 0:
                print('You have not made any order at this hotel')
            else:
                for i in range(len(list_of_order)):
                    print(i + 1, list_of_order[i])
                code = input('Choose order to delete: ')
                code = list_of_order[int(code) - 1]
                sock.send(code.encode())
                ans = sock.recv(1024).decode()
                if ans == 'OK':
                    ans = sock.recv(1024).decode()
                    if ans == 'OK':
                        print('Cancel successfully')
                    else:
                        print('It is over 24 hours, you cannot delete your order')
                elif ans == 'Not found':
                    print('Not found')
        elif m_choices == '3':
            list_of_hot = sock.recv(1024).decode()
            list_of_hot = eval(list_of_hot)
            print(list(list_of_hot))
        else: 
            break
    
        
def clogin():
    ans = input('Username: ')
    username = ans
    sock.send(ans.encode())
    ans = input('Password: ')
    sock.send(ans.encode())
    ans = sock.recv(1024).decode()
    if ans == 'OK':
        print('Login success')
        menu(username)
    else:
        print('Login fail')

def csignup():
    ans = input('Username: ')
    sock.send(ans.encode())
    ans = input('Password: ')
    sock.send(ans.encode())
    ans = input('Bank account no: ')
    sock.send(ans.encode())
    ans = sock.recv(1024).decode()
    if ans == 'OK':
        print('Sign up success')
        start_menu()
    else:
        print('Sign up fail')

def start_menu():
    choices = ['0. Exit', '1. Login', '2. Sign up']
    for i in choices:
        print(i)
    choose = input('Your choice: ')

    if choose == '1':
        sock.send('1'.encode())
        clogin()
    elif choose == '2':
        sock.send('2'.encode())
        csignup()
    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('You are connecting to', HOST, PORT)
sock.connect((HOST, PORT))

start_menu()

sock.close()
