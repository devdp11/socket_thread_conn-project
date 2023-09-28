import socket
import threading

clients = {}
disconnected_clients = {}  # Manter o registro de clientes desconectados

# Função para lidar com as mensagens de um cliente
def handle_client_input(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            
            full_message = f"{client_name}: {message}"
            print(f"{full_message}")
            
            for other_client_socket, other_client_name in clients.items():
                if other_client_socket != client_socket:
                    other_client_socket.send(full_message.encode())
        except:
            break
    
    # Move o cliente para o registro de clientes desconectados quando a conexão é encerrada
    del clients[client_socket]
    disconnected_clients[client_socket] = client_name
    client_socket.close()

def handle_client_output(client_socket):
    while True:
        pass

# Configurações do servidor
host = socket.gethostname()
port = 12345

ip = socket.gethostbyname(host)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((ip, port))

server_socket.listen(5)

print(f"Server Alocated on IP: {ip} with the door: {port}")

while True:
    # Aceita uma conexão quando um cliente se conecta
    client_socket, client_address = server_socket.accept()
    client_name = client_socket.recv(1024).decode()
    
    print(f"Connection established with the client {client_address} --> Welcome {client_name}")
    
    if client_socket in disconnected_clients:
        clients[client_socket] = disconnected_clients[client_socket]
        del disconnected_clients[client_socket]
    
    clients[client_socket] = client_name
    
    input_thread = threading.Thread(target=handle_client_input, args=(client_socket, client_name))
    input_thread.start()
    
    output_thread = threading.Thread(target=handle_client_output, args=(client_socket,))
    output_thread.start()
