import socket
import threading
from conversation import conversation
import time

# This is a Dictionary of all the current objects,
# where each Object's Key in the dictionary is the conversation's ID
conversation_objects = {}

def listener(server_socket):
    while True:
        data, client_address = server_socket.recvfrom(4096)
        if data:
            string_data = data.decode()
            
            # extract client ID
            client_id = string_data[0:4]

            # check client ID against list of ongoing conversations (here this will call a checker function,
            # that returns a pointer or reference to a pre-existing or new conversation object)
            conversation_object = conversation_checker(client_id)

            # send message to corresponding conversation (using corresponding reference returned from checker function)
            conversation_object.receive_packet(string_data[4:])

            #print(f"{client_address}, id {client_id}")
            server_socket.sendto(b"ACKed", client_address) # here for now, will be in tcp functions later



def conversation_checker(client_id):
    # Check if conversation already exists
    object_reference = conversation_objects.get(client_id)

    if object_reference is not None:
        #print(f"Found pre-existing conversation {object_reference.conversation_id}")
        return object_reference
    else:
        # Create a new conversation object
        object_reference = conversation(client_id)
        conversation_objects[client_id] = object_reference
        return object_reference
