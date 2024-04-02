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

    # Create initial Hello Pckt packet
    hello = packet.Pckt(
        Header = packet.PcktHeader(
            Magic = globals.MAGIC,
            Checksum = 0,
            ConvID = globals.own_conv_id,
            SequenceNum = 0,
            Final = True,
            Type = packet.PacketType.Data
        ),
        # string just for testing
        Body = consensus.encode_Hello(
            consensus.PcktHello(
                ID = consensus.PcktID.hello_c2s,
                Version = 0,
                NumFeatures = 0,
                Feature = bytes()
            )
        )
    )

    temp = bytearray(packet.encode_packet(hello))
    
    temp[4:8] = struct.pack('!I', zlib.crc32(temp[8:]))

        while len(globals.conversation_objects) == 0:
            globals.own_socket.sendto(bytes(synPckt_bytes), server_address)
            time.sleep(1)

    
    # START CLI here
    

start_client()
    