import socket
from rdt import rdt_send
from rdt import rdt_receive
from rdt import PacketType
# python TCP server skeleton
# 1. Get hostname using socket.gethostname() method
# 2. Specify por to listen on
# 3. Create socket object using socket.socket() method
# 4. Bind the host and the port number using bind() method
# 5. Call listen() method (you can configure how many clients the server can listen to simultaneously)
# 6. Establish connection with client using accept() method
# 7. Send message to client using the send() method
# 8. Close connection using the close() method

# We need to make this UDP, since UDP is connectionless we
# need to find another way to send and receive



def server():

    try:
        #host = socket.gethostname()

        host = '0.0.0.0'

        port = 51664

        convid = 1
        
        #s = socket.socket()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Host is {host} ")

        s.bind((host, port)) # tuple notation

        print(f" Listening on port {port}")

        data = " "

        while data.lower().strip() != "exit":

            # Receive data from client (up to 1024 bytes) and decode it
            #rcvpkt, client_address = s.recvfrom(1024)


            # If no data is received, then break from loop
            
            #decoded_data = data.decode()
            data, client_address = rdt_receive(s, convid)

            print(f"Received from client: {data}")

            # Get user response as input and send to client after encoding
            #response = input("Enter response to send to client: ")
            #response = "Response from Server!"

            #rdt_send(response, s, client_address, convid, PacketType.Data)

            #s.sendto(sndpkt, client_address)

    except Exception as e:

       print(f"Error: {e}")

    #finally:

        #c.close()


if __name__ == "__main__":

    server()
