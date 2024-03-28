import socket
import threading
from conversation import conversation
import time
import packet

# This is a Dictionary of all the current objects,
# where each Object's Key in the dictionary is the conversation's ID
conversation_objects = {}

def listener(server_socket):
    while True:
        data, client_address = server_socket.recvfrom(4096)
        if data:
            # Extract Packet Header
            pckt_header = packet.decode_header(data[:20])

            # check convID against list of ongoing conversations (here this will call a checker function,
            # that returns a pointer or reference to a pre-existing or new conversation object)
            conversation_object = conversation_checker(pckt_header.ConvID)

            # send message to corresponding conversation (using corresponding reference returned from checker function)
            conversation_object.receive_packet(data[20:])



def conversation_checker(client_id):
    # Check if conversation already exists
    object_reference = conversation_objects.get(client_id)

    if object_reference is not None:
        return object_reference
    else:
        # Create a new conversation object
        object_reference = conversation(client_id)
        conversation_objects[client_id] = object_reference
        return object_reference
