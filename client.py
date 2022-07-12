import socket

HOST = '127.0.0.1'
PORT = 8000


def clogin():
    ans = input('Username: ')
    sock.send(ans.encode())
    ans = input('Password: ')
    sock.send(ans.encode())
    checklogin = sock.recv(1024).decode()
    if checklogin == '1':
        print('Login successful')
        return True
    if checklogin == '0':
        print('Login fail')
        return False


def csignup():
    ans = input('Username: ')
    sock.send(ans.encode())
    ans = input('Password: ')
    sock.send(ans.encode())
    ans = input('Bank account no: ')
    sock.send(ans.encode())
    checksignup = sock.recv(1024).decode()
    if checksignup == '1':
        print('Sign up successful')
        return True
    if checksignup == '0':
        print('Sign up fail')
        return False


 def menu():
    print('1.Login\t 2.Sign up')
    choose = input()
    if choose == '1':
        sock.send('1'.encode())
    if choose == '2':
        sock.send('2'.encode())

            
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('You are connecting to', HOST, PORT)
sock.connect((HOST, PORT))
menu()

sock.close()
