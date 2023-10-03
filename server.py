import socket
import threading
from datetime import datetime
import os

# Dicionário para rastrear os clientes conectados / Variável para rastrear o número máximo de clientes / Semáforo para controlar o acesso à variável max_clients
clients = []
max_clients = 2
max_clients_lock = threading.Semaphore(1)

def handle_thread(message, client_socket):
    for client in clients:
        if client[1] != client_socket:
            try:
                client[1].send(message.encode("utf-8"))
            except:
                remove_client(client[1])

def remove_client(client_socket):
    for client in clients:
        if client[1] == client_socket:
            clients.remove(client)
            
def handle_input(client_socket, client_name, client_address):
    time = datetime.now().strftime("%d-%m-%Y %H:%M")
    while True:
        try:
            # Aqui, o server tenta receber a mensagem enviada pelo cliente e descodifica, mesmo que seja da opção 1, 2 ou 3
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
       
            elif message.startswith("chat"):
                print(f"{client_name}-[{client_address}] has entered the universal chat!")
                while True:
                    msg = client_socket.recv(1024).decode("utf-8")

                    if not msg or msg == "/return":
                        print(f"{client_name}-[{client_address}] has left the universal chat!")
                        break
                    else:
                        handle_thread(f"{client_name}: {msg}", client_socket)
                        print(f"[{time}] - Message sent by client {client_name}-[{client_address}]: {msg}")

        except Exception as e:
            print(f"An Error has appeared: {e}")
            break

    # Quando a conexão do cliente é terminada, o mesmo é removido da lista do clientes e é liberado acesso a novos clientes
    with max_clients_lock:
        for idx, client in enumerate(clients):
            if client[0] == client_name and client[1] == client_socket:
                clients.pop(idx)
                client_socket.close()
                print(f"Connection ended with the client [{client_address}] --> Goodbye {client_name}")

def handle_server():
    host = socket.gethostname()
    port = 12345
    ip = socket.gethostbyname(host)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(2)

    os.system('cls')
    print(f"Server Alocated on IP: {ip} with port: {port}")

    while True:
        # Código para aceitar uma conexão quando o cliente se autentica
        client_socket, client_address = server_socket.accept()

        with max_clients_lock:
            if len(clients) >= max_clients:
                print(f"Connection refused from [{client_address}] - Maximum number of clients reached.")
                client_socket.close()
                continue
            else:
                client_name = client_socket.recv(1024).decode("utf-8")
                client_address = f"{ip}:{port}"

                print(f"Connection established with the client [{client_address}] --> Welcome {client_name}")
                # Store the client as a tuple (client_name, client_socket) in the clients list
                clients.append((client_name, client_socket))

        # Criação de uma thread para lidar com as mensagens do cliente
        client_thread = threading.Thread(target=handle_input, args=(client_socket, client_name, client_address))
        client_thread.start()

handle_server()