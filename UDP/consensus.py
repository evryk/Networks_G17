from enum import Enum
from dataclasses import dataclass
from typing import List
import uuid
import struct

MAGIC = 0x01051117

class PcktID(Enum):
    hello_c2s = 0  # from client to server, basically SYN
    hello_back_s2c = 1  # from server to client, basically ACK
    vote_c2s_request_vote = 2  # from client to server to begin vote
    vote_s2c_broadcast_question = 3  # from server to all clients to vote on
    vote_c2s_response_to_question = 4  # from client to server
    vote_s2c_broadcast_result = 5  # from server to all clients

@dataclass
class DataHeader:
    Magic: int  # 4 bytes
    Checksum: int  # 4 bytes CRC32
    PcktID: PcktID  # 2 bytes


# Hello Packet
class HelloPacket(Enum):
    voting = 0
    file_transfer = 1

@dataclass
class PcktHello:
    Header: DataHeader  # 8 bytes
    Version: int  # 4 bytes
    NumFeatures: int  # 2 bytes
    Feature: List[int]  # num_features*2 bytes

PcktHelloResponse = PcktHello


# Vote Begin Request
class Response(Enum):
    UNSAT = 0
    SAT = 1
    SYNTAX_ERROR = 2
    TIMEOUT = 3

@dataclass
class PcktVoteRequest:
    Header: DataHeader  # 8 bytes
    VoteID: uuid.UUID  # 16 bytes # uuid.uuid4() # str(uuid.uuid4()) # uuid.uuid4().hex
    QuestionLength: int  # 4 bytes
    Question: str  # QuestionLength bytes long

PcktVoteBroadcast = PcktVoteRequest

@dataclass
class PcktVoteResponse:
    Header: DataHeader  # 8 bytes
    VoteID: uuid.UUID  # 16 bytes
    Response: Response  # 2 bytes

PcktVoteResultBroadcast = PcktVoteResponse

#How can I iterate through a byte array, and extract certain bytes to decode and assign to each parameter in my classes? How do I encode these parameters back into bytes?

def encode_dataHeader(header):
    return struct.pack('!IIH', header.Magic, header.Checksum, header.PcktID.value)

def decode_dataHeader(data):
    magic, checksum, pckt_id = struct.unpack('!IIH', data[:10])
    return DataHeader(Magic=magic, Checksum=checksum, PcktID=PcktID(pckt_id))


# PcktHello
def encode_Hello(packet):
    header = encode_dataHeader(packet.Header)
    features = b''.join(struct.pack('!H', feature) for feature in packet.Feature)
    return struct.pack('!10sIH' + 'H'*len(features), header, packet.Version, packet.NumFeatures, *features)

def decode_Hello(data):
    header = decode_dataHeader(data[:10])
    version, num_features = struct.unpack('!IH', data[10:16])
    features = [struct.unpack('!H', data[i:i+2])[0] for i in range(16, 16 + 2*num_features, 2)]
    return PcktHello(Header=header, Version=version, NumFeatures=num_features, Feature=features)


# PcktHelloResponse
def encode_HelloResponse(packet):
    header = encode_dataHeader(packet.Header)
    features = b''.join(struct.pack('!H', feature) for feature in packet.Feature)
    return struct.pack('!10sIH' + 'H'*len(features), header, packet.Version, packet.NumFeatures, *features)

def decode_HelloResponse(data):
    header = decode_dataHeader(data[:10])
    version, num_features = struct.unpack('!IH', data[10:16])
    features = [struct.unpack('!H', data[i:i+2])[0] for i in range(16, 16 + 2*num_features, 2)]
    return PcktHelloResponse(Header=header, Version=version, NumFeatures=num_features, Feature=features)

# 