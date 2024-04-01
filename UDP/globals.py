import socket

# Variables and Constants for Global use
own_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

own_conv_id = 0

MAGIC = 0x01051117

# This is a Dictionary of all the current objects,
# where each Object's Key in the dictionary is the conversation's ID
conversation_objects = {}