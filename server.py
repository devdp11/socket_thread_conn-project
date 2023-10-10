import socket
import threading
from datetime import datetime
import os

# Dicionário para armazenar os clientes conectados / Dicionário para armazenar os usernames dos clientes conectados / Variável para encontrar o número máximo de clientes / Semáforo para controlar o acesso à variável max_clients
clients = []
usernames = []
max_clients = 2
max_clients_lock = threading.Semaphore(1)

time = datetime.now().strftime("%d-%m-%Y %H:%M")

def handle_thread(message, client_socket):
    for client in clients:
        if client[1] != client_socket:
            try:
                client[1].send(message.encode("utf-8"))
            except:
                remove_client(client[1])

def remove_client(client_socket, client_name):
    for client in clients:
        if client[1] == client_socket:
            clients.remove(client)
            usernames.remove(client_name)
            
def handle_input(client_socket, client_name, client_address):
    while True:
        try:
            # Aqui, o server tenta receber a mensagem enviada pelo cliente e descodifica, mesmo que seja da opção 1, 2 ou 3
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break

            if message.startswith("calc-op: "):
                calc_operation = message[len("calc-op: "):]
                try:
                    res = eval(calc_operation)
                    res_str = str(res)
                    client_socket.send(f"calc-res: {res_str}".encode("utf-8"))
                    print(f'[{time}] - Operation result made by client {client_name}-[{client_address}]: {res_str}')
                except Exception as e: # Envio do erro
                    client_socket.send(f"calc-res: Error: {e}".encode("utf-8"))

            elif message.startswith("chat"):
                print(f"[{time}] - {client_name}-[{client_address}] has entered the universal chat!")
                while True:
                    msg = client_socket.recv(1024).decode("utf-8")

                    if not msg or msg == "/return":
                        print(f"[{time}] - {client_name}-[{client_address}] has left the universal chat!")
                        break
                    else:
                        handle_thread(f"{client_name}: {msg}", client_socket)
                        print(f"[{time}] - Message sent by client {client_name}-[{client_address}]: {msg}")

            elif message.startswith('list'):
                client_socket.send("\nConnected Clients:\n".encode('utf-8') + ", ".join(usernames).encode('utf-8'))
                
            else:
                # Senão for mensagem de calculo, é enviado uma mensagem para o cmd, com o nome do cliente que a enviou e o conteúdo da mensagem
                full_message = f"[{time}] - Message sent by client {client_name}-[{client_address}]: {message}"
                client_socket.send(f"Message has been received".encode("utf-8"))
                print(f"{full_message}")

        except Exception as e:
            print(f"An Error has appeared: {e}")
            break

    # Quando a conexão do cliente é terminada, o mesmo é removido da lista do clientes e é liberado acesso a novos clientes
    with max_clients_lock:
        for idx, client in enumerate(clients):
            if client[0] == client_name and client[1] == client_socket:
                clients.pop(idx)
                client_socket.close()
                print(f"[{time}] - Connection ended with the client [{client_address}] --> Goodbye {client_name}")
                usernames.remove(client_name)

def handle_server():
    host = socket.gethostname()
    port = 12345
    ip = socket.gethostbyname(host)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(2)

    os.system('cls')
    print(f"[{time}] - Server Alocated on IP: {ip} with port: {port}")

    while True:
        # Código para aceitar uma conexão quando o cliente se autentica
        client_socket, client_address = server_socket.accept()

        with max_clients_lock:
            if len(clients) >= max_clients:
                print(f"[{time}] - Connection refused from [{client_address}] - Maximum number of clients reached.")
                client_socket.close()
                continue
            else:
                client_name = client_socket.recv(1024).decode("utf-8")
                client_address = f"{ip}:{port}"

                print(f"[{time}] - Connection established with the client [{client_address}] --> Welcome {client_name}")
                # Armazenar um cliente num tuple (client_name, client_socket) na lista clients
                clients.append((client_name, client_socket))
                usernames.append(client_name)

        # Criação de uma thread para lidar com as mensagens do cliente
        client_thread = threading.Thread(target=handle_input, args=(client_socket, client_name, client_address))
        client_thread.start()

handle_server()