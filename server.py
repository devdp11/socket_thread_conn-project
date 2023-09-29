import socket
import threading

# Dicionário para rastrear os clientes conectados
clients = {}

# Função para lidar com as mensagens enviadas por um cliente
def handle_client_input(client_socket, client_name, client_address):
    while True:
        try:
            # Aqui, o server tenta receber a mensagem enviada pelo cliente e descodifica, mesmo que seja da opção 1 (Messenger) ou 2 (Calculadora)
            # Se não for "true", volta para o menu
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            
            # Neste caso, quando a mensagem começa "startswitch" com calc_result, é enviado um print a dizer que esta mensagem é proveniente da calculadora, e que cliente fez a operação matemática
            if message.startswith("calc_result: "):
                calc_result = message[len("calc_result: "):]
                print(f"The value of the operation made by {client_name} is: {calc_result}")
            else:

                # Senão for mensagem de calculo, é enviado uma mensagem para o cmd, com o nome do cliente que a enviou e o conteúdo da mensagem
                full_message = f"{client_name}: {message}"
                print(f"{full_message}")

            # Enviar a mensagem para todos os clientes conectados
            for other_client_socket in clients.values():
                if other_client_socket != client_socket:
                    other_client_socket.send(full_message.encode("utf-8"))
        except Exception as e:
            print(f"An Error has appeared: {e}")
            break

    # Quando a conexão do cliente é terminada, o mesmo é removida da lista do clients
    del clients[client_name]
    client_socket.close()
    print(f"Connection ended with the client {client_address} --> Goodbye {client_name}")

def handle_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((ip, port))

    server_socket.listen(5)

    print(f"Server Alocated on IP: {ip} with the door: {port}")

    while True:
        # Código para aceitar uma conexão quando o cliente se conecta
        client_socket, client_address = server_socket.accept()
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

handle_server()
