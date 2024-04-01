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

def start_client():
    server_address = ("localhost", 8080) # IP, port

    # create single listener thread
    listener_thread = threading.Thread(target=listener, args=( ))
    listener_thread.start()

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
            print("pinging")
            globals.own_socket.sendto(bytes(PingPckt_bytes), server_address)
            time.sleep(1)


    print(f"My ConvID is {globals.own_conv_id}\n")

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

    
    # START CLI here
    

start_client()
    