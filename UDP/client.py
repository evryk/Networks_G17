import socket
import random
import time

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    server_address = ("localhost", 8080) # IP, port


    # create unique conversation ID
    id = random.randint(1000, 9999)

    while True:
        # send ID and message
        message = str(id) + input("Your message: ")
        client_socket.sendto(message.encode(), server_address)
        
        # receive ACK
        response, _ = client_socket.recvfrom(4096) # recvfrom returns data and address (address not necessary)
        print(response.decode())

    client_socket.close()

start_client()
