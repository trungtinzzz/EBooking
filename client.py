from secrets import choice
import tkinter as tk
import json
import socket
import datetime
import pickle

from click import option

HOST = '127.0.0.1'
PORT = 8003

class StartPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="LOG IN", anchor=tk.CENTER)
        label_user = tk.Label(self, text="username ", anchor=tk.CENTER)
        label_pswd = tk.Label(self, text="password ", anchor=tk.CENTER)

        self.label_notice = tk.Label(self,text="",bg="bisque2", anchor=tk.CENTER)
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')

        button_log = tk.Button(self,text="LOG IN", command=lambda: appController.clogin(self, sock)) 
        button_log.configure(width=10)
        button_sign = tk.Button(self,text="SIGN UP", command=lambda: appController.showPage(SignUpPage)) 
        button_sign.configure(width=10)
        
        label_title.grid(row= 0, column= 0)
        label_user.grid(row= 1, column= 0)
        self.entry_user.grid(row= 2, column= 0)
        label_pswd.grid(row= 3, column= 0)
        self.entry_pswd.grid(row= 4, column= 0)
        self.label_notice.grid(row= 5, column= 0)

        button_log.grid(row= 6, column= 0)
        button_sign.grid(row= 6, column= 1)

class SignUpPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="SIGN UP", anchor=tk.CENTER)

        label_user = tk.Label(self, text="username ", anchor=tk.CENTER)
        label_pswd = tk.Label(self, text="password ", anchor=tk.CENTER)
        label_bank = tk.Label(self, text="bank number ", anchor=tk.CENTER)


        self.label_notice = tk.Label(self,text="",bg="bisque2", anchor=tk.CENTER)
        self.entry_user = tk.Entry(self,width=20,bg='light yellow')
        self.entry_pswd = tk.Entry(self,width=20,bg='light yellow')
        self.entry_bank = tk.Entry(self,width=20,bg='light yellow')

        button_sign = tk.Button(self,text="SIGN UP", command=lambda: appController.csignup(self, sock)) 
        button_sign.configure(width=10)
        
        label_title.grid(row= 0, column= 0)
        label_user.grid(row= 1, column= 0)
        self.entry_user.grid(row= 2, column= 0)
        label_pswd.grid(row= 3, column= 0)
        self.entry_pswd.grid(row= 4, column= 0)
        label_bank.grid(row= 5, column= 0)
        self.entry_bank.grid(row= 6, column= 0)
        self.label_notice.grid(row= 7, column= 0)

        button_sign.grid(row= 8, column= 0)

class HomePage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="HOME PAGE", anchor=tk.CENTER)

        btn_list = tk.Button(self,text="HOTEL LIST", command=lambda: appController.showPage(ListPage)).grid(row = 0, column = 0)
        btn_info = tk.Button(self,text="YOUR BOOKING INFO", command=lambda: appController.showPage(InfoPage)).grid(row = 0, column = 1)
        btn_booking = tk.Button(self,text="BOOKING HOTEL", command=lambda: appController.showPage(StartPage)).grid(row = 0, column = 2)

        btn_logout = tk.Button(self, text="LOG OUT", command=lambda: appController.showPage(StartPage))

        label_title.grid(row= 0, column= 0)
        btn_list.grid(row= 1, column= 0)        
        btn_info.grid(row= 1, column= 1)        
        btn_booking.grid(row= 1, column= 2)        
        btn_logout.grid(row= 2, column= 0)  

class ListPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="HOTEL LIST", anchor=tk.CENTER)
        
        label_title.grid(row= 0, column= 0)
        appController.show_list_hol(self,sock)

        btn_quit = tk.Button(self,text="Back", command=lambda: appController.showPage(HomePage))
        btn_quit.grid(row= 1, column=0)
class InfoPage(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        label_title = tk.Label(self, text="YOUR BOOKING INFO", anchor=tk.CENTER)
        label_title.grid(row= 0, column= 0)

        #load account's order data
        file_of_order = open('data/order.json')
        raw_order_list = json.load(file_of_order)


class App(tk.Tk):
    def __init__(self): 
        tk.Tk.__init__(self)

        self.title("E-Booking")
        self.geometry("500x200")
        self.resizable(width=False, height=False)

        container = tk.Frame()
        container.configure(bg="grey")

        container.pack(side="top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (StartPage, HomePage, SignUpPage, ListPage, InfoPage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame 


        self.frames[StartPage].tkraise()
        
    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()

    def clogin(self,curFrame,sck: socket):
        #get username and password
        username = curFrame.entry_user.get()
        password = curFrame.entry_pswd.get()

        if username == "" or password == "":
            curFrame.label_notice["text"] = "Fields cannot be emty"
            return
        
        #send cmd option
        option = "LOGIN"
        sck.send(option.encode()) 

        #send account info
        sck.send(username.encode())
        sck.send(password.encode())

        #recv login check
        login = sck.recv(1024).decode()
        if login == 'Fail':
            curFrame.label_notice["text"] = "Login fail"
            return
        else:
            curFrame.label_notice["text"] = "Login success"
            self.showPage(HomePage)

    def csignup(self,curFrame,sck: socket):
        #get account info
        username = curFrame.entry_user.get()
        password = curFrame.entry_pswd.get()
        bankno = curFrame.entry_bank.get()

        if username == "" or password == "" or bankno == "":
            curFrame.label_notice["text"] = "Fields cannot be emty"
            return
        
        #send cmd option
        option = "SIGNUP"
        sck.send(option.encode()) 

        #send account info
        sck.send(username.encode())
        sck.send(password.encode())
        sck.send(bankno.encode())

        #recv signup check
        signup = sck.recv(1024).decode()
        if signup == 'Fail':
            curFrame.label_notice["text"] = "Sign up fail"
            return
        else:
            curFrame.label_notice["text"] = "Sign up success"
            self.showPage(StartPage) 

    def show_list_hol(self,curFrame,sck: socket):
        option = "LIST"
        sck.send(option.encode()) 

        list_of_hot = sck.recv(1024).decode()
        list_of_hot = eval(list_of_hot)
        print(list(list_of_hot))
    
    def show_info_ord(self,curFrame,sck: socket):
        option = "INFO"
        sck.send(choice.encode())

        file_of_order = open('data/order.json')
        raw_order_list = json.load(file_of_order)
        file_of_order.close()

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
        
def menu():
    while True:
        menu_choices = ['0. Exit', '1. Search for room', '2. Cancel order', '3. List of hotels']
        for i in menu_choices:
            print(i)
        m_choices = input('Your choice: ')
        sock.send(m_choices.encode())
        if m_choices == '1':
            ans = input('Hotel name: ')
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
            ans = sock.recv(1024).decode()
            if ans == 'OK':
                list_of_room = sock.recv(1024).decode()
                list_hot = eval(list_of_room)
                list_of_no = []
                for i in list_hot:
                    print('No.:' , i['no'])
                    print('Number of bed:', i['kind'])
                    print('Description:', i['des'])
                    print('Price:', i['price'], 'dollar a night')
                    list_of_no.append(i['no'])
                print("-"*20)
                booking_menu(list_of_no)
            elif ans == 'Fail':
                print('Not found')
        elif m_choices == '2':
            ans = input('Hotel name: ')
            sock.send(ans.encode())
            ans = sock.recv(1024).decode()
            if ans == 'OK':
                print('Cancel successfully')
            elif ans == 'Not found':
                print('Not found')
            else:
                print('It is over 24 hours, you can not cancel your order')
        elif m_choices == '3':
            list_of_hot = sock.recv(1024).decode()
            list_of_hot = eval(list_of_hot)
            print(list(list_of_hot))
        else: 
            break
    

# def start_menu():
#     choices = ['0. Exit', '1. Login', '2. Sign up']
#     for i in choices:
#         print(i)
#     choose = input('Your choice: ')

#     if choose == '1':
#         sock.send('1'.encode())
#         clogin()
#     elif choose == '2':
#         sock.send('2'.encode())
#         csignup()
    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('You are connecting to', HOST, PORT)
sock.connect((HOST, PORT))

#start_menu()

app = App()
app.showPage(StartPage)
app.mainloop()
sock.close()
