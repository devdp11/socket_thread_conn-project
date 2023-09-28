import socket
import os

# Configurações do cliente
host = socket.gethostname()
port = 12345

HEADER_LENGTH = 10

ip = socket.gethostbyname(host)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((ip, port))

name = input('Introduce your name:')
client_socket.send(name.encode())

while True:
    print('1 - Messenger')
    print('2 - Calculator')
    print('0 - Quit')
    op1 = int(input('Choose an option:'))

    if op1 == 1:
        while True:
            message = input("Enter your message (type '/return' to go back to menu): ")
            if message == "/return":
                break
            client_socket.send(message.encode())

    elif op1 == 2:
        n1 = float(input('Introduce the first number:'))
        n2 = float(input('Introduce the second number:'))
        
        while True:
            print('1 - Add')
            print('2 - Sub')
            print('3 - Div')
            print('4 - Mul')
            print('0 - Return')
            op2 = int(input('Choose an option:'))

            if op2 == 1:
                value = n1 + n2
                client_socket.send(str(value).encode())
                break
            elif op2 == 2:
                value = n1 - n2
                client_socket.send(str(value).encode())
                print(f'O valor da conta: {value}')
                break
            elif op2 == 3:
                value = n1 / n2
                client_socket.send(str(value).encode())
                break
            elif op2 == 4:
                value = n1 * n2
                client_socket.send(str(value).encode())
                break
            elif op2 == 0:
                break
            else:
                print('Choose a valid option!')

    elif op1 == 0:
        response = input('Are you sure you want to leave the application? (y/n)')
        if response == 'y':
            print('Leaving the program ...')
            client_socket.close()
            os.system('cls')
            break

    else:
        print('Choose a valid option:')
