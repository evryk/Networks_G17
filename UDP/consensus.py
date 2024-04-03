from enum import Enum
from dataclasses import dataclass
from typing import List
import uuid
import struct

class PcktID(Enum):
    hello_c2s = 0  # from client to server, basically SYN
    hello_back_s2c = 1  # from server to client, basically ACK
    vote_c2s_request_vote = 2  # from client to server to begin vote
    vote_s2c_broadcast_question = 3  # from server to all clients to vote on
    vote_c2s_response_to_question = 4  # from client to server
    vote_s2c_broadcast_result = 5  # from server to all clients


# Hello Packet
class HelloPacket(Enum):
    voting = 0
    file_transfer = 1

@dataclass
class PcktHello:
    DataID: PcktID  # 2 bytes
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
    DataID: PcktID  # 2 bytes
    VoteID: uuid.UUID  # 16 bytes
    QuestionLength: int  # 4 bytes
    Question: str  # QuestionLength bytes long

PcktVoteBroadcast = PcktVoteRequest

@dataclass
class PcktVoteResponse:
    DataID: PcktID  # 2 bytes
    VoteID: uuid.UUID  # 16 bytes
    Response: Response  # 2 bytes

PcktVoteResultBroadcast = PcktVoteResponse


# Decoding the PcktID has to be done separately, so we know which packet was sent
# no point encoding the PcktID separately as the sender knows which packet to send
def decode_pcktID(data: bytes) -> PcktID:
    value, = struct.unpack('!H', data[:2])
    return PcktID(value)


# PcktHello
def encode_Hello(packet : PcktHello):
    # Convert the list of features into bytes directly in the struct.pack call
    return struct.pack('!HIH' + 'H'*packet.NumFeatures, packet.DataID.value, packet.Version, packet.NumFeatures, *packet.Feature)

def decode_Hello(data : bytes):
    pckt_id = decode_pcktID(data[:2])
    version, num_features = struct.unpack('!IH', data[2:8])
    features = [struct.unpack('!H', data[i:i+2])[0] for i in range(8, 8 + 2*num_features, 2)]
    return PcktHello(DataID=pckt_id, Version=version, NumFeatures=num_features, Feature=features)


# PcktHelloResponse
def encode_HelloResponse(packet : PcktHelloResponse):
    # Convert the list of features into bytes directly in the struct.pack call
    return struct.pack('!HIH' + 'H'*packet.NumFeatures, packet.DataID.value, packet.Version, packet.NumFeatures, *packet.Feature)

def decode_HelloResponse(data : bytes):
    pckt_id = decode_pcktID(data[:2])
    version, num_features = struct.unpack('!IH', data[2:8])
    features = [struct.unpack('!H', data[i:i+2])[0] for i in range(8, 8 + 2*num_features, 2)]
    return PcktHelloResponse(DataID=pckt_id, Version=version, NumFeatures=num_features, Feature=features)


# PcktVoteRequest
def encode_VoteRequest(packet : PcktVoteRequest):
    pckt_id = struct.pack('!H', packet.DataID.value)
    vote_id = packet.VoteID.bytes # Encode the VoteID as bytes
    question_length = struct.pack('!I', packet.QuestionLength)
    question = packet.Question.encode('utf-8') # Encode the Question as bytes
    # Concatenate all the parts together:
    return pckt_id + vote_id + question_length + question 

def decode_VoteRequest(data : bytes):
    pckt_id = decode_pcktID(data[:2])
    vote_id = uuid.UUID(bytes=data[2:18])
    question_length, = struct.unpack('!I', data[18:22])
    question = data[22:22+question_length].decode('utf-8')
    return PcktVoteRequest(DataID=pckt_id, VoteID=vote_id, QuestionLength=question_length, Question=question)


# PcktVoteBroadcast
def encode_VoteBroadcast(packet : PcktVoteBroadcast):
    pckt_id = struct.pack('!H', packet.DataID.value)
    vote_id = packet.VoteID.bytes
    question_length = struct.pack('!I', packet.QuestionLength)
    question = packet.Question.encode('utf-8')
    return pckt_id + vote_id + question_length + question 

def decode_VoteBroadcast(data : bytes):
    pckt_id = decode_pcktID(data[:2])
    vote_id = uuid.UUID(bytes=data[2:18])
    question_length, = struct.unpack('!I', data[18:22])
    question = data[22:22+question_length].decode('utf-8')
    return PcktVoteBroadcast(DataID=pckt_id, VoteID=vote_id, QuestionLength=question_length, Question=question)


# PcktVoteResponse
def encode_VoteResponse(packet : PcktVoteResponse):
    pckt_id = struct.pack('!H', packet.DataID.value)
    vote_id = packet.VoteID.bytes
    response = struct.pack('!H', packet.Response.value) # 2 bytes
    # Concatenate all the parts together
    return pckt_id + vote_id + response

def decode_VoteResponse(data : bytes):
    pckt_id = decode_pcktID(data[:2])
    vote_id = uuid.UUID(bytes=data[2:18])
    response = struct.unpack('!H', data[18:20])[0]
    # Return a new PcktVoteResponse object
    return PcktVoteResponse(DataID=pckt_id, VoteID=vote_id, Response=Response(response))


# PcktVoteResultBroadcast
def encode_ResultBroadcast(packet : PcktVoteResultBroadcast):
    pckt_id = struct.pack('!H', packet.DataID.value)
    vote_id = packet.VoteID.bytes
    response = struct.pack('!H', packet.Response.value)
    # Concatenate all the parts together
    return pckt_id + vote_id + response

def decode_ResultBroadcast(data : bytes):
    pckt_id = decode_pcktID(data[:2])
    vote_id = uuid.UUID(bytes=data[2:18])
    response = struct.unpack('!H', data[18:20])[0]
    # Return a new PcktVoteResultBroadcast object
    return PcktVoteResultBroadcast(DataID=pckt_id, VoteID=vote_id, Response=Response(response))