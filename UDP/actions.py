# Based on PcktID --> consensus.py file
import consensus
from enum import Enum
import uuid

# Defing SYN function for Client to server.
def SYN_send():
    pass

# Defining SYN_ACK function for Server to Client
def SYN_ACK():
    pass

# Defining Vote Request Packet - initial question client to server
def VoteRequest(question, Enum): #Header possibly or conversation ID

    number = consensus.PcktID(Enum) # vote_c2s_request_vote = 2 , number which will be called upon from the PcktID(Enum)

    #Assuming Question is already defined as a string 
    vote_request = consensus.PcktVoteRequest(
            Header = "Actual Header", # This will be the header which the client sends, obviously not what is in the brackets 
            VoteID = uuid.uuid4(), # Generating a UUID for vote identification
            QuestionLength=len(question), # Question string length 
            Question = question # Actual question
        )
    
    # Encode the message which is to be sent accross 
    encoded_message = consensus.encode_VoteRequest(vote_request)

    return encoded_message # The server will now broadcast this encoded question to all of the clients on the server 
    #pass

# Defining Vote Broadcast Packet - server to all client nodes
def VoteBroadcast(encoded_question, Enum):

    number = consensus.PcktID(Enum) # vote_c2s_request_vote = 3 , number which will be called upon from the PcktID(Enum)
    vote_request = consensus.PcktVoteBroadcast

    # Decode the message sent from the client
    vote_request = consensus.decode_VoteRequest(encoded_question) # Decode the message so that we can confirm if it has been transferred correctly.

    # Print the parameters of question. 
    print("Received vote request for question: ", vote_request.Question)
    print("Vote ID and question length: ", vote_request.VoteID, vote_request.QuestionLength)
    
    # Encode the question to be sent to the clients 
    encoded_broadcast = consensus.encode_VoteBroadcast(vote_request)
    return encoded_broadcast # Encoded broadcast to be sent to all of the clients 
    # pass

# Defining Vote Response Packet - all client nodes to server
def VoteResponse(encoded_broadcast, Enum):
    
    number = consensus.PcktID(Enum) # vote_c2s_request_vote = 4 , number which will be called upon from the PcktID(Enum)

    #Decode the question that has just been broadcasted 
    vote_response = consensus.decode_VoteBroadcast(encoded_broadcast)
    
    #Use Z3 to calculate the correct answer, the correct answer will then be decoded and returned by the function. 
    pass

# Defining Vote Result Broadcast Packet - server to all client nodes
def ResultBroadcast(encoded_response, Enum):

    number = consensus.PcktID(Enum) # vote_c2s_request_vote = 4 , number which will be called upon from the PcktID(Enum)

    # Decode result and could possibly print maybe, message will be send back to original client based on correct answer. 
    
    pass


