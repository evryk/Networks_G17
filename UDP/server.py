import socket
import threading
from listener import listener
import time
import globals
import random

def start_server():
    server_address = ('localhost', 8080) # IP, port
    globals.own_socket.bind(server_address)

    print("Server is listening on port 8080")

    # create unique conversation ID
    globals.own_conv_id = random.randint(1000, 9999)
    print(f"My ConvID is {globals.own_conv_id}\n")

    # create single listener thread
    listener_thread = threading.Thread(target=listener, args=( ))
    listener_thread.start()

if __name__ == "__main__":
    start_server()
