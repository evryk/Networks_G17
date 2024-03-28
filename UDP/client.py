import socket
from rdt import rdt_send
from rdt import rdt_receive
from rdt import PacketType
# 1. (optional) get hostname of client using socket.gethostname()
# 2. Create socket object using socket.socket() module
# 3. Connect to local host by passing port number and hostname of server
# 4. Send and receive message from the server using send() and recv()
# 5. Close the connection with server

def client():

    host = socket.gethostname()

    port = 51664
    
    address = (host, port)

    convid = 1

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #message = input("Enter your message (Type 'exit' to exit): ")
    message = ""

    while message.lower().strip() != "exit":

        message = input("Enter your message (Type 'exit' to exit): ")

        works = rdt_send(message, client_socket, address, convid, PacketType.Data)

        #client_socket.sendto(sndpkt, (host, port))

        #rcvpkt, server_address = client_socket.recvfrom(256)

        #data, address = rdt_receive(client_socket, convid)

        #print(f"Received from server: {data}")


    client_socket.close()


if __name__ == "__main__":
    client()
