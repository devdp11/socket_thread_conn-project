import socket
import threading

# Dicionário para rastrear os clientes conectados
clients = {}

# Variável para rastrear o número máximo de clientes
max_clients = 2

# Semáforo para controlar o acesso concorrente à variável max_clients
max_clients_lock = threading.Semaphore(1)

# Função para lidar com as mensagens enviadas por um cliente
def handle_client_input(client_socket, client_name, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            
            if message.startswith("calc_operation: "):
                calc_operation = message[len("calc_operation: "):]
                try:
                    # Realiza a operação de cálculo
                    res = eval(calc_operation)
                    res_str = str(res)
                    client_socket.send(f"calc_result: {res_str}".encode("utf-8"))
                    print(f'The final result of the calculation is: {res_str}')
                except Exception as e:
                    client_socket.send(f"calc_result: Error: {e}".encode("utf-8"))
            else:
                full_message = f"{client_name}: {message}"
                print(f"{full_message}")

            for other_client_socket in clients.values():
                if other_client_socket != client_socket:
                    other_client_socket.send(full_message.encode("utf-8"))
        except Exception as e:
            print(f"An Error has appeared: {e}")
            break

    # Quando a conexão do cliente é terminada, o mesmo é removida da lista do clients
    with max_clients_lock:
        del clients[client_name]
        client_socket.close()
        print(f"Connection ended with the client {client_address} --> Goodbye {client_name}")

def handle_server():
    print(f"Server Alocated on IP: {ip} with the door: {port}")

    while True:
        # Código para aceitar uma conexão quando o cliente se conecta
        client_socket, client_address = server_socket.accept()

        with max_clients_lock:
            if len(clients) >= max_clients:
                print(f"Connection refused from {client_address} - Maximum number of clients reached.")
                client_socket.close()
                continue
            else:
                client_name = client_socket.recv(1024).decode("utf-8")

                client_address = f"{ip}:{port}"

                print(f"Connection established with the client {client_address} --> Welcome {client_name}")

                clients[client_name] = client_socket  # Adicione o cliente à lista de clientes
                print(clients)

        # Inicie uma nova thread para lidar com as mensagens do cliente
        client_thread = threading.Thread(target=handle_client_input, args=(client_socket, client_name, client_address))
        client_thread.start()

# Configurações do servidor
host = socket.gethostname()
port = 12345
ip = socket.gethostbyname(host)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((ip, port))

server_socket.listen(2)

handle_server()
