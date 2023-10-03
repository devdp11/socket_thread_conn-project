import socket
import os

def menu():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = 12345
    ip = socket.gethostbyname(host)

    client_socket.connect((ip, port))

    os.system('cls')
    name = input('Introduce your username:')
    client_socket.send(name.encode("utf-8"))

    while True:
        os.system('cls')
        print('1 - Message to Server')
        print('2 - Math Operations')
        print('0 - Quit')
        op1 = int(input('Choose an option:'))

        if op1 == 1:
            os.system('cls')
            while True:
                # Aqui, aparece um input para o client introduzir uma mensagem quando escolhe a opção 1 do menu inicial que lhe aparece quando se autentica ao server.
                # Caso escrever uma mensagem, esta é codificada usando o algoritmo "utf-8" e é enviada para o server, onde será transmitida no cmd
                message = input("Write your message (Type /return to leave): ")
                if message.lower() == "/return":
                    break
                else:
                    client_socket.send(f"{message}".encode("utf-8"))
                    server_response = client_socket.recv(1024).decode("utf-8")
                    if server_response.startswith("Message has been received"):
                        print(server_response)

        elif op1 == 2:
            os.system('cls')
            while True:
                operation = input('Write an mathematic operation (Type /return to leave):')
                if operation.lower() == "/return":
                    break
                else:
                    try:
                        # Envia a operação de cálculo para o servidor
                        client_socket.send(f"calc-op: {operation}".encode("utf-8"))    
                        # Após o envio da operação para o servidor, esperasse a resposta dessa mesma operação que irá ser recebida aqui e demonstrada no cmd
                        result_message = client_socket.recv(1024).decode("utf-8")
                        if result_message.startswith("calc-res: "):
                            os.system('cls')
                            calc_result = result_message[len("calc-res: "):]
                            print(f'The final result of the operation is: {calc_result}')
                        else:
                            print(f"Unexpected response from server: {result_message}")
                    except Exception as e:
                        print(f"Error: {e}")

        elif op1 == 0:
            os.system('cls')
            # Quando o cliente escolhe a ultima opção, é perguntado se deseja mesmo sair do programa e caso escolha "y", o socket da close à ligação entre o cliente e o servidor e a consola é limpa, usando a biblioteca os.
            response = input('Want to leave the application? (y/n):')
            if response == 'y':
                client_socket.close()
                os.system('cls')
                break
        else:
            print('Choose a valid option:')

menu()