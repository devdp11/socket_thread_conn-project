import socket
import threading

# Dicionário para rastrear os clientes conectados
clients = {}

# Função para lidar com as mensagens enviadas por um cliente
def handle_client_input(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            
            full_message = f"{client_name}: {message}"
            print(f"{full_message}")
            
            # Enviar a mensagem para todos os clientes conectados
            for other_client_socket in clients.values():
                if other_client_socket != client_socket:
                    other_client_socket.send(full_message.encode())
        except:
            break

    # Quando o cliente desconecta, removê-lo da lista de clientes
    del clients[client_name]
    client_socket.close()
    print(f"Connection ended with the client {client_address} --> Goodbye {client_name}")

# Configurações do servidor
host = socket.gethostname()
port = 12345
ip = socket.gethostbyname(host)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((ip, port))

server_socket.listen(5)

print(f"Server Alocated on IP: {ip} with the door: {port}")

while True:
    # Código para aceitar uma conexão quando o cliente se conecta
    client_socket, client_address = server_socket.accept()
    client_name = client_socket.recv(1024).decode()
    
    client_address = f"{ip}:{port}"

    print(f"Connection established with the client {client_address} --> Welcome {client_name}")
    
    clients[client_name] = client_socket  # Adicione o cliente à lista de clientes

    # Inicie uma nova thread para lidar com as mensagens do cliente
    client_thread = threading.Thread(target=handle_client_input, args=(client_socket, client_name))
    client_thread.start()
