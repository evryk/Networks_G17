from dataclasses import dataclass
from enum import Enum
import struct

class PacketType(Enum):
    Data = 0
    ACK = 1
    NACK = 2

@dataclass
class PcktHeader:
    Magic: int  # 4 bytes
    Checksum: int  # 4 bytes CRC32
    ConvID: int  # 4 bytes
    SequenceNum: int  # 4 bytes
    Final: int # 2 bytes
    Type: PacketType  # 2 bytes

@dataclass
class Pckt:
    Header: PcktHeader  # 20 bytes
    Body: bytes  # N bytes
    # 20 + N <= 256 Bytes



# Unpack the header bytes
def decode_header(header_bytes):
    magic, checksum, convid, seqnum, final, ptype = struct.unpack('!IIIIHH', header_bytes)
    return PcktHeader(magic, checksum, convid, seqnum, final, PacketType(ptype))

# Unpack whole packet including the body
def decode_packet(packet_bytes):
    header = decode_header(packet_bytes[:20])
    body = packet_bytes[20:]
    return Pckt(header, body)


# Pack the header
def encode_header(header: PcktHeader):
    return struct.pack('!IIIIHH', header.Magic, header.Checksum, header.ConvID, header.SequenceNum, header.Final, header.Type.value)

# Pack whole packet including the body
def encode_packet(packet: Pckt):
    header_bytes = encode_header(packet.Header)
    body_bytes = packet.Body
    return header_bytes + body_bytes
