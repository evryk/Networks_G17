import socket
import threading
from conversation import conversation
import time
import packet
from rdt import rdt_receive

# This is a Dictionary of all the current objects,
# where each Object's Key in the dictionary is the conversation's ID
conversation_objects = {}

def listener(server_socket):
    while True:
      #data, client_address = server_socket.recvfrom(4096)
        data, client_address = rdt_receive(server_socket)
        if data:
            # Extract Packet Header
            pckt_header = data.Header

            # check client ID against list of ongoing conversations (here this will call a checker function,
            # that returns a pointer or reference to a pre-existing or new conversation object)
            conversation_object = conversation_checker(pckt_header.ConvID)

            # send message to corresponding conversation (using corresponding reference returned from checker function)
            conversation_object.receive_packet(data.Body)



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
