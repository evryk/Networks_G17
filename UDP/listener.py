import globals
from conversation import conversation
import packet
import zlib


def listener():
    while True:
        data, client_address = globals.own_socket.recvfrom(4096)
        if data:
            # Extract Packet Header
            pckt_header = packet.decode_header(data[:20])

            # Check Magic
            if pckt_header.Magic != globals.MAGIC:
                # Drop the packet, corruption in Magic field detected
                continue

            # Generate Checksum and compare
            if pckt_header.Checksum != zlib.crc32(data[8:]):
                # Drop the packet, corruption in Checksum field detected
                continue

            # check convID against list of ongoing conversations (here this will call a checker function,
            # that returns a pointer or reference to a pre-existing or new conversation object)
            conversation_object = conversation_checker(pckt_header.ConvID)

            # Make sure conversation_object is not an empty reference
            if conversation_object == None:
                continue

            # Save client_address to conversation object, for sending purposes
            conversation_object.updateIP(client_address)

            # send message to corresponding conversation (using corresponding reference returned from checker function)
            conversation_object.receive_packet(data)



def conversation_checker(client_id):
    # Check if conversation already exists
    object_reference = globals.conversation_objects.get(client_id)

    if object_reference is not None:
        return object_reference
    else:
        # Create a new conversation object
        object_reference = conversation(client_id)
        globals.conversation_objects[client_id] = object_reference
        return object_reference
