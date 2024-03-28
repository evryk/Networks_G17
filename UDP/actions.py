# Based on PcktID --> consensus.py file
import consensus
from enum import Enum
import uuid
import packet


class VoteManager:
    def __init__(self):
        pass

    # Defing SYN function for Client to server.
    def SYN_send():
        #SYN packet to be sent to the server 
        syn_packet = consensus.PcktHello(
            # Header = packet.DataHeader(MAGIC=packet.MAGIC, Checksum=0, PcktID=consensus.PcktID.hello_c2s),
            ID = 0,
            Version = 1,
            NumFeatures = 0,
            Feature = []
        )

        #Encode the packet to be sent to the server 
        syn_packet_data = consensus.encode_Hello(syn_packet)
        print("SYN sent")
        return syn_packet_data

    # Defining SYN_ACK function for Server to Client
    def SYN_ACK(syn_packet_data):
        
        syn_packet_decoded = consensus.decode_Hello(syn_packet_data)

        if syn_packet_decoded.ID == 0:
            print("SYN recieved")
            syn_packet_decoded = consensus.PcktHelloResponse(
            #   Header = packet.DataHeader(MAGIC=packet.MAGIC, Checksum=0, PcktID=consensus.PcktID.hello_back_s2c),
                ID = 1,
                Version = 1,
                NumFeatures = 0,
                Feature = []
            )
            syn_ack_encoded = consensus.decode_HelloResponse(syn_packet_decoded)

            return syn_ack_encoded
        else:
            print("Unexpected response, handshake failed")
            return None

    # Defining Vote Request Packet - initial question client to server
    def VoteRequest(question): #Header possibly or conversation ID

        # number_return = consensus.PcktID(number) # vote_c2s_request_vote = 2 , number which will be called upon from the PcktID(Enum)

        #Assuming Question is already defined as a string 
        vote_request = consensus.PcktVoteRequest(
            # Header = "Actual Header", # This will be the header which the client sends, obviously not what is in the brackets 
                VoteID = str(uuid.uuid4()), # Generating a UUID for vote identification
                QuestionLength=len(question), # Question string length 
                Question = question # Actual question
            )
        
        # Encode the message which is to be sent accross 
        encoded_message = consensus.encode_VoteRequest(vote_request)

        return encoded_message # The server will now broadcast this encoded question to all of the clients on the server 


    # Defining Vote Broadcast Packet - server to all client nodes
    def VoteBroadcast(encoded_question):

        # number_return = consensus.PcktID(number) # vote_c2s_request_vote = 3 , number which will be called upon from the PcktID(Enum)
        vote_request = consensus.PcktVoteBroadcast

        # Decode the message sent from the client
        vote_request = consensus.decode_VoteRequest(encoded_question) # Decode the message so that we can confirm if it has been transferred correctly.

        # Print the parameters of question. 
        print("Received vote request for question: ", vote_request.Question)
        print("Vote ID and question length: ", vote_request.VoteID, vote_request.QuestionLength)
        
        # Encode the question to be sent to the clients 
        encoded_broadcast = consensus.encode_VoteBroadcast(vote_request)
        return encoded_broadcast # Encoded broadcast to be sent to all of the clients 


    # Defining Vote Response Packet - all client nodes to server
    def VoteResponse(encoded_broadcast):
        
        # number_return = consensus.PcktID(number) # vote_c2s_request_vote = 4 , number which will be called upon from the PcktID(Enum)

        #Decode the question that has just been broadcasted 
        vote_response = consensus.decode_VoteBroadcast(encoded_broadcast)
        
        #Use Z3 to calculate the correct answer, the correct answer will then be decoded and returned by the function. 
        pass

    # Defining Vote Result Broadcast Packet - server to all client nodes
    def ResultBroadcast(encoded_response):

        number = consensus.PcktID(Enum) # vote_c2s_request_vote = 4 , number which will be called upon from the PcktID(Enum)

        # Decode result and could possibly print maybe, message will be send back to original client based on correct answer. 
        
        pass


