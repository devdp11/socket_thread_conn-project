import socket
import threading

def menu():
    while True:
        print('1 - Messenger')
        print('2 - Calculator')
        print('0 - Quit')
        op1 = int(input('Choose a option:'))

        if op1 == 1:
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket, name))
            receive_thread.start()

            while True:
                message = input()
                if message == "/return":
                    break
                client_socket.send(message.encode())

        elif op1 == 2:
            while True:
                print('1 - Add')
                print('2 - Sub')
                print('3 - Div')
                print('4 - Mul')
                print('0 - Return')
                op2 = int(input('Choose a option:'))

                if op2 == 1:
                    pass
                elif op2 == 2:
                    pass
                elif op2 == 3:
                    pass
                elif op2 == 4:
                    pass
                elif op2 == 0:
                    break
                else:
                    print('\nChoose a valid option!')

        elif op1 == 0:
            response = input('Are you sure you want to leave the application? (y/n)')
            if response == 'y':
                print('Leaving the program ...')
                client_socket.close()
                return  
            elif response == 'n':
                continue 

        else:
            print('\nChoose a valid option!')

def receive_messages(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(f"{message}")
            print()
        except:
            break

# Configurações do cliente
host = socket.gethostname()
port = 12345

ip = socket.gethostbyname(host)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((ip, port))

name = input('Introduce your name:')
client_socket.send(name.encode())

menu()