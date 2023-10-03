import socket
import os
import threading
from datetime import datetime

in_chat = False

def recv_msg(client_socket):
    global in_chat
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if in_chat:
                print(message)
        except Exception as e:
            print(f"Error has appeared {e}")
            break

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = socket.gethostname()
    port = 12345
    ip = socket.gethostbyname(host)
    client_socket.connect((ip, port))

    os.system('cls')
    name = input('Introduce your username:')
    client_socket.send(name.encode("utf-8"))
    return client_socket

def menu(client_socket):
    global in_chat
    receive_thread = threading.Thread(target=recv_msg, args=(client_socket,))
    receive_thread.start()

    while True:
        os.system('cls')
        print('1 - Send Messages')
        print('0 - Quit')
        op1 = int(input('Choose an option:'))

        if op1 == 1:
            os.system('cls')
            in_chat = True
            if in_chat:
                client_socket.send("chat".encode("utf-8"))
                print("You entered the chat (Type /return to leave)")
                while True:
                    message = input()
                    
                    if in_chat:  # Verifique se ainda está no chat antes de enviar mensagens
                        client_socket.send(f"{message}".encode("utf-8"))
                        if message.lower() == "/return":
                            in_chat = False  # Define in_chat como False ao sair do chat
                            break

        elif op1 == 0:
            os.system('cls')
            response = input('Want to leave the application? (y/n):')
            if response == 'y':
                client_socket.close()
                os.system('cls')
                break
        else:
            print('Choose a valid option:')

if __name__ == "__main__":
    client_socket = connect_to_server()
    menu(client_socket)