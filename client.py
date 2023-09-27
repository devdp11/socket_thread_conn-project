import socket
import threading

def menu():
    while True:
        print('\n1 - Messenger')
        print('2 - Calculator')
        print('3 - Quit')
        option = int(input('Choose a option:'))
        print()

        if option == 1:
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket, name))
            receive_thread.start()

            while True:
                message = input()
                if message == "/return":
                    break  # Retorna ao menu principal das 3 opções
                print(f"Eu: {message}")
                client_socket.send(message.encode())

        elif option == 2:
            print('calculadora')

        elif option == 3:
            response = input('Are you sure you want to leave the application? (y/n)')
            if response == 'y':
                print('\nLeaving the program ...')
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
        except:
            break

# Configurações do cliente
host = socket.gethostname()
port = 12345

ip = socket.gethostbyname(host)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((ip, port))

name = input('\nIntroduce your name:')
client_socket.send(name.encode())

menu()