import socket
import threading

def handle_client(client_socket, client_address):
    data = client_socket.recv(1024)
    while (data):
        string_data = data.decode()
        print(f"{client_address}: {string_data}")
        client_socket.send(b"ACKed")
        data = client_socket.recv(1024)
    client_socket.close()

    print("Client killed")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 8080)
    server_socket.bind(server_address)

    server_socket.listen(1)
    print("Server is listening on port 8080")

    while True:
        print("Waiting for a connection")
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
