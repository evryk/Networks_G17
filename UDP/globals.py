import socket
import random
import vote
import conversation

# Variables and Constants for Global use
own_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

own_conv_id = 0

MAGIC = 0x01051117

# This is a Dictionary of all the current objects,
# where each Object's Key in the dictionary is the conversation's ID
conversation_objects = {}

# Vote Manager reference
vote_manager_ref: vote.VoteManager

# Conversations Manager reference
conv_manager: conversation.conversations_manager

# Generate new conversation ID for client
generatedIDs = {}

def generate_convID():
    newID = 0

    while newID == 0 or generatedIDs.get(newID):
        newID = random.randint(1, 0xFFFFFFFF)
    
    generatedIDs[newID] = newID
    return newID