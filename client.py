import socket
import threading

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

name = input('Introduce your name:')
client_socket.send(name.encode())

# Inicia uma thread para receber mensagens do servidor continuamente
receive_thread = threading.Thread(target=receive_messages, args=(client_socket, name))
receive_thread.start()

# Agora o cliente pode enviar mensagens para o servidor e outros clientes
while True:
    message = input()
    print(f"Eu: {message}")
    client_socket.send(message.encode())