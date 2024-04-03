import globals
from conversation import conversation
import packet
import zlib
import struct


def listener():
    while True:
        data, client_address = globals.own_socket.recvfrom(4096)
        if data:
            # Extract Packet Header
            pckt_header = packet.decode_header(data[:24])

            # Check Magic
            if pckt_header.Magic != globals.MAGIC:
                # Drop the packet, corruption in Magic field detected
                continue

            # Generate Checksum and compare
            if pckt_header.Checksum != zlib.crc32(data[8:]):
                # Drop the packet, corruption in Checksum field detected
                continue

            # IS THIS A PING REQUEST?
            if pckt_header.Type == packet.PacketType.PING_REQ or pckt_header.ConvID == 0:
                PingResPckt = packet.Pckt(
                    Header=packet.PcktHeader(
                        Magic = globals.MAGIC,
                        Checksum = 0,
                        ConvID = globals.generate_convID(),
                        PacketNum = 0,
                        SequenceNum = 0,
                        Final = True,
                        Type = packet.PacketType.PING_RES
                    ),
                    Body=bytes()
                )

                PingResPckt_bytes = bytearray(packet.encode_packet(PingResPckt))
                PingResPckt_bytes[4:8] = struct.pack('!I', zlib.crc32(PingResPckt_bytes[8:]))
                globals.own_socket.sendto(bytes(PingResPckt_bytes), client_address)
                continue

            # Get unique Conversation ID allocated by Server to Client
            if pckt_header.Type == packet.PacketType.PING_RES:
                globals.own_conv_id = pckt_header.ConvID
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
