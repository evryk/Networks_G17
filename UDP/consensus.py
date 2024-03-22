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

@dataclass
class PcktHeader:
    Magic: int  # 4 bytes
    Checksum: int  # 4 bytes CRC32
    PcktID: PcktID  # 2 bytes


# Hello Packet
class HelloPacket(Enum):
    voting = 0
    file_transfer = 1

@dataclass
class PcktHello:
    Header: PcktHeader  # 8 bytes
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
    Header: PcktHeader  # 8 bytes
    VoteID: uuid.UUID  # 16 bytes
    QuestionLength: int  # 4 bytes
    Question: str  # QuestionLength bytes long

PcktVoteBroadcast = PcktVoteRequest

@dataclass
class PcktVoteResponse:
    Header: PcktHeader  # 8 bytes
    VoteID: uuid.UUID  # 16 bytes
    Response: Response  # 2 bytes

PcktVoteResultBroadcast = PcktVoteResponse
