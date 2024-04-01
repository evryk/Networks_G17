import socket
import threading
import random
import globals
import time
import packet
from conversation import conversation
from listener import listener
import consensus
import struct
import zlib
import sys
# Import the command line interface

from command_line_interface import commandlineinterface

def start_client():
    server_address = ("localhost", 8080) # IP, port

    # create unique conversation ID
    globals.own_conv_id = random.randint(1000, 9999)
    print(f"My ConvID is {globals.own_conv_id}\n")

    # create single listener thread
    listener_thread = threading.Thread(target=listener, args=( ))
    listener_thread.start()

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

    # Command line interface example
    cli = commandlineinterface()
    cli.run()
    # Returns the question which the person has asked, we could return the packet here or could manipulate this question in order to be a part of the packet.
    question = cli.question
    print(F"Question is ", question)

    temp = bytearray(packet.encode_packet(hello))
    
    temp[4:8] = struct.pack('!I', zlib.crc32(temp[8:]))

    globals.own_socket.sendto(bytes(temp), server_address)
    

start_client()
    