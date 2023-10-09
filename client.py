import socket
import os
import threading

in_chat = False

def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = socket.gethostname()
    port = 12345
    ip = socket.gethostbyname(host)
    client_socket.connect((ip, port))

    os.system('cls')
    name = input('Introduce your username:')
    client_socket.send(name.encode("utf-8"))
    return client_socket
    
def recv_msg(client_socket):
    global in_chat
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if in_chat:
                print(message)
        except Exception as e:
            print(f"An Error has appeared {e}")
            break

def main(client_socket):
    global in_chat

    while True:
        os.system('cls')
        print('1 - Chat with clients')
        print('2 - Chat to server')
        print('3 - Math calculator')
        print('4 - List connected clients')
        print('0 - Quit')
        op1 = int(input('Choose an option:'))

        if op1 == 1:
            os.system('cls')
            in_chat = True
            if in_chat:
                client_socket.send("chat".encode("utf-8")) 
                print("You entered the chat (Type /return to leave)")
                receive_thread = threading.Thread(target=recv_msg, args=(client_socket,))
                receive_thread.start()
                while True:
                    message = input()
                    client_socket.send(f"{message}".encode("utf-8"))
                    if message.lower() == "/return":
                        in_chat = False
                        break
        elif op1 == 2:
            os.system('cls')
            while True:
                message = input("Write your message (Type /return to leave): ")
                if message.lower() == "/return":
                    break
                else:
                    client_socket.send(f"{message}".encode("utf-8"))
                    server_response = client_socket.recv(1024).decode("utf-8")
                    if server_response.startswith("Message has been received"):
                        print(server_response)
        elif op1 == 3:
            os.system('cls')
            while True:
                operation = input('Write a mathematical operation (Type /return to leave):')
                if operation.lower() == "/return":
                    break
                else:
                    try:
                        client_socket.send(f"calc-op: {operation}".encode("utf-8"))    
                        result_message = client_socket.recv(1024).decode("utf-8")
                        if result_message.startswith("calc-res: "):
                            os.system('cls')
                            calc_result = result_message[len("calc-res: "):]
                            print(f'The final result of the operation is: {calc_result}')
                        else:
                            print(f"Unexpected response from server: {result_message}")
                    except Exception as e:
                        print(f"Error: {e}")
        elif op1 == 4:
            os.system('cls')
            client_socket.send(f"list".encode("utf-8"))
            
            # Aqui o cliente vai receber a lista dos usernames dos clientes conectados e armazena os numa variável para depois ser exposta no cmd
            clients_list = client_socket.recv(1024).decode("utf-8")
            print(clients_list)
            input("Press Enter to continue...")

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
    client_socket = connect()
    main(client_socket)