import socket
import threading
from listener import listener

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    server_address = ('172.20.10.4', 8080) # IP, port
    server_socket.bind(server_address)

    print("Server is listening on port 8080")

    # create single listener thread
    listener_thread = threading.Thread(target=listener, args=(server_socket, ))
    listener_thread.start()

if __name__ == "__main__":
    start_server()
