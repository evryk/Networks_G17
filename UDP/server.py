import threading
from listener import listener
import globals
import vote

def start_server():
    server_address = ('localhost', 8080) # IP, port
    globals.own_socket.bind(server_address)

    print("\nServer is listening on port 8080\n")

    # create unique conversation ID
    globals.own_conv_id = globals.generate_convID()
    print(f"My ConvID is {globals.own_conv_id}\n")

    # create single listener thread
    listener_thread = threading.Thread(target=listener, args=( ))
    listener_thread.start()

    # Initialize Vote Manager
    globals.vote_manager_ref = vote.VoteManager()

if __name__ == "__main__":
    start_server()
