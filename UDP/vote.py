import threading
import globals
import consensus
import conversation
import statistics
import uuid


# Class for a specific Vote
class Vote:
    def __init__(self, vote_id : uuid.UUID, q):
        # Vote credentials
        self.voteID = vote_id

        # Question at the heart of the Vote
        self.question = q

        # Dictionary of responses (each key/index is a conversation id)
        self.responses = {}



# Class for managing all Votes
class VoteManager:
    def __init__(self):
        # Dictionary for votes I'm hosting (keys are VoteID, holds Vote Class)
        self.my_votes = {}
        self.my_votes_lock = threading.Lock()

        # Dictionary for votes I'm taking part in (keys are VoteID, holds Responses)
        self.voted_for = {}
        self.voted_for_lock = threading.Lock()
        

    # Server received PcktVoteRequest
    def startVote(self, pckt : consensus.PcktVoteRequest):

        with self.my_votes_lock:            
            # Check for duplicates
            dup = self.my_votes.get(pckt.VoteID)
            if dup is not None:
                return

            # Create new Vote object that will be broadcasted to all clients
            self.my_votes[pckt.VoteID] = Vote(pckt.VoteID, pckt.Question)

            # Set up client nodes participating in Vote
            for conv in globals.conversation_objects:
                globals.conversation_objects[conv].send_VoteBroadcast(pckt.VoteID, pckt.Question)


    # Client received PcktVoteBroadcast
    def respondToQuestion(self, receivedFrom : conversation, pckt : consensus.PcktVoteBroadcast):

        with self.voted_for_lock:
            # Check for duplicates
            dup = self.voted_for.get(pckt.VoteID)
            if dup is not None:
                return

            # Temporary test variable
            ans: int
            try:
                ans = eval(pckt.Question.strip())
            except: 
                print("Error with eval function")
                ans = 2 # Syntax Error

            # Save Response in voted_for dictionary for given VoteID
            self.voted_for[pckt.VoteID] = int(ans)
            print(f"My response is: {ans}\n")

            # Send Response to server
            receivedFrom.send_VoteResponse(pckt.VoteID, ans)
    

    # Server received PcktVoteResponse
    def computeResult(self, convID, pckt : consensus.PcktVoteResponse):
        
        with self.my_votes_lock: 
            # Check for duplicates
            dup = self.my_votes[pckt.VoteID].responses.get(convID)
            if dup is not None:
                return
            
            # Add response for each convID (key) to Vote Class
            self.my_votes[pckt.VoteID].responses[convID] = pckt.Response

            # Check if we gathered Responses from at least 75% of Clients
            if len(self.my_votes[pckt.VoteID].responses) >= 3/4 * len(globals.conversation_objects):
                # Compute Result
                result = statistics.multimode(self.my_votes[pckt.VoteID].responses.values())[0]
                print(f"VoteID: {pckt.VoteID} -> Result : {result}\n")

                # Broadcast Consensus Response to all nodes participating
                for conv in globals.conversation_objects:
                    globals.conversation_objects[conv].send_BroadcastResult(pckt.VoteID, result)
    
    
    # Client got official result from server
    def receivedResult(self, pckt : consensus.PcktVoteResultBroadcast):
        
        with self.voted_for_lock: 
            # Make sure we have voted for this
            if self.voted_for.get(pckt.VoteID) is not None:
                # Check if consensus agrees with us
                if pckt.Response != self.voted_for[pckt.VoteID]:
                    print(f"Consensus disagrees with us, Consensus result: {pckt.Response}\n")
                    self.voted_for[pckt.VoteID] = pckt.Response

                else: 
                    print(f"Consensus agrees with us!!!")
                    print(f"Result: {pckt.Response}\n")
