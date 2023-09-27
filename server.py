import socket
import threading

clients = {}

# Função para lidar com as mensagens de um cliente
def handle_client(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            
            for other_client_socket, other_client_name in clients.items():
                if other_client_socket != client_socket:
                    full_message = f"{client_name}: {message}"
                    other_client_socket.send(full_message.encode())
                    
                    print(f"{full_message}")
        except:
            break
    
    # Remove o cliente quando a conexão é encerrada
    del clients[client_socket]
    client_socket.close()

# Configurações do servidor
host = socket.gethostname()
port = 12345

ip = socket.gethostbyname(host)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((ip, port))

server_socket.listen(5)

print(f"\nServer Alocated on IP: {ip} with the door: {port}\n")

while True:
    # Aceita uma conexão quando um cliente se conecta
    client_socket, client_address = server_socket.accept()
    client_name = client_socket.recv(1024).decode()
    
    print(f"Connection established with the client {client_address} --> Welcome {client_name}\n")
    
    # Adiciona o cliente à lista de clientes
    clients[client_socket] = client_name
    
    # Inicia uma thread para lidar com as mensagens deste cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
    client_thread.start()
