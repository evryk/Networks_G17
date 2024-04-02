import threading
import globals
import time
import packet
from listener import listener
import struct
import zlib
import vote
import sys
# Import the command line interface
from command_line_interface import commandlineinterface

def start_client():
    # server_address = ("localhost", 8080) # IP, port
    server_address = ("localhost", 8080) # IP, port
    # Create single listener thread
    listener_thread = threading.Thread(target=listener, args=( ))
    listener_thread.start()

    # Initialize Vote Manager
    globals.vote_manager_ref = vote.VoteManager()

    # Send initial Ping Request to obtain unique ConvID
    if globals.own_conv_id == 0:
        PingPckt = packet.Pckt(
            Header=packet.PcktHeader(
                Magic = globals.MAGIC,
                Checksum = 0,
                ConvID = globals.own_conv_id,
                SequenceNum = 0,
                Final = True,
                Type = packet.PacketType.PING_REQ
            ),
            Body=bytes()
        )

        PingPckt_bytes = bytearray(packet.encode_packet(PingPckt))
        PingPckt_bytes[4:8] = struct.pack('!I', zlib.crc32(PingPckt_bytes[8:]))

        while globals.own_conv_id == 0:
            globals.own_socket.sendto(bytes(PingPckt_bytes), server_address)
            time.sleep(1)


    # Obtained Conversation ID
    print(f"My ConvID is {globals.own_conv_id}\n")

    # Send SYN packet to initialize conversation with server
    if len(globals.conversation_objects) == 0:
        synPckt = packet.Pckt(
            Header=packet.PcktHeader(
                Magic = globals.MAGIC,
                Checksum = 0,
                ConvID = globals.own_conv_id,
                SequenceNum = 0,
                Final = True,
                Type = packet.PacketType.SYN
            ),
            Body=bytes()
        )

        synPckt_bytes = bytearray(packet.encode_packet(synPckt))
        synPckt_bytes[4:8] = struct.pack('!I', zlib.crc32(synPckt_bytes[8:]))

        while len(globals.conversation_objects) == 0:
            globals.own_socket.sendto(bytes(synPckt_bytes), server_address)
            time.sleep(1)

    time.sleep(1)
    # START CLI here
    # Command line interface 
    cli = commandlineinterface()
    cli.run()
    # Returns the question which the person has asked, we could return the packet here or could manipulate this question in order to be a part of the packet.
    question = cli.question
    print(F"Your question is '", question, "', sending this to the server.")
    # We will now initialize the handshake, the packet sending of the question is afterwards. This is simply an example of how the question would be encoded. 
    if len(question) != 0:
        question_packet = packet.Pckt(
            Header = packet.PcktHeader(
                Magic = globals.MAGIC,
                Checksum = 0,
                ConvID =globals.own_conv_id,
                SequenceNum = 2, 
                Final = True,
                Type = packet.PacketType.Data
            ),
            Body = bytes(question, 'utf-8')
        )

start_client()
    