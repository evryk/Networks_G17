import socket
import threading
from listener import listener
import time

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    server_address = ('172.20.10.4', 8080) # IP, port
    server_socket.bind(server_address)

    print("Server is listening on port 8080")

    # create single listener thread

    data, client_address = server_socket.recvfrom(1024)
    if data == b'SYN':
     print("SYN received from client:", client_address)
     time.sleep(1)

# Step 2: Send SYN-ACK
    server_socket.sendto(b'SYN-ACK', client_address)
    print("SYN-ACK sent")
    time.sleep(1)
# Step 3: Receive ACK
    data, _ = server_socket.recvfrom(1024)
    if data == b'ACK':
        print("ACK received from client:", client_address)
        print("Three-way Handshake completed. Communication established.")
       # return server_socket

    else:
        print("Unexpected response. Handshake failed.")
        return None


    listener_thread = threading.Thread(target=listener, args=(server_socket, ))
    listener_thread.start()

if __name__ == "__main__":
    start_server()
