import socket
import threading

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 8080)
    client_socket.connect(server_address)

    while(1):
        message = input("Your message: ")
        client_socket.send(message.encode())
        response = client_socket.recv(4096)
        print(response.decode())

    client_socket.close()

start_client()
