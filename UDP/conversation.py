import threading
import time
import packet
import globals
import zlib
import struct
import consensus
import random
import uuid


class conversations_manager:
    def __init__(self):
        # Start cleaner thread
        self.thread_reference = threading.Thread(target=self.cleaner, args=())
        self.thread_reference.start()

    def __del__(self):
        self.thread_reference.join()

    def cleaner(self):
        while (1):
            time.sleep(1)
            for conv in globals.conversation_objects:
                if globals.conversation_objects[conv].markedForDeletion:
                    globals.conversation_objects[conv].main_loop_bool = False
                    globals.conversation_objects[conv].thread_reference.join()
                    print(f"Deleting node {globals.conversation_objects[conv].conversation_id}.")
                    del globals.conversation_objects[conv]
                    print("Current Number of ongoing Conversations: ", len(globals.conversation_objects))
                    break


class conversation:
    def __init__(self, own_id):
        # Save the client ID
        self.conversation_id = own_id
        print(f"Conversation {self.conversation_id} created.\n")

        # Save Client IP address and port
        self.client_address = ("", 0)


        # Sending ###########################################
        # Sliding Window, holding already packaged packets ready to send
        self.sliding_window = {}

        # Dictionary of state of ack confirmation for sent packets - boolean type (SeqNums we have ACKs for)
        self.acks_for_sent = {}

        # Timer Dictionary (record of timestamps at time of sending)
        self.timers = {}

        # Used with all the sending variables
        self.sending_lock = threading.Lock()
        self.sr_function_lock = threading.Lock()

        # Sliding window parameters
        self.windowBottom = 0
        self.windowSize = 5
        self.largestPacketNum = 0


        # Receiving #########################################
        # This is where new packets arrive in the conversation
        self.buffer = []

        # Used with the buffer
        self.buffer_lock = threading.Lock()

        # Dictionary of received packets - boolean type
        self.received = {}

        # Used with the received packets boolean dictionary
        self.received_lock = threading.Lock()

        # Keeps track of highest received packet number
        self.previousPacketNum = 0

        # Keeps track of when was the last time this node contacted us
        self.lastContact = int(time.time() * 1000)
        
        # If this reaches a 100 this node is being disconnected
        self.missedCalls = 0
        self.markedForDeletion = False
        self.main_loop_bool = True


        # Start main loop thread
        self.thread_reference = threading.Thread(target=self.main_loop, args=( ))
        self.thread_reference.start()

        # Send initial Hello
        self.send_HelloPckt()


    def updateIP(self, new_address):
        # Update IP address of node we're sending to
        self.client_address = new_address


    def receive_packet(self, bytes):
        # Update last contact
        self.lastContact = int(time.time() * 1000)
        self.missedCalls = 0
        self.markedForDeletion = False

        # Decode full packet
        Pckt = packet.decode_packet(bytes)

        # Check PacketType
        match Pckt.Header.Type:
            case packet.PacketType.Data:
                # Update received boolean dictionary
                with self.received_lock:
                    # Send ACK
                    self.send_ACK(Pckt.Header.PacketNum)

                    # Duplicate check
                    dup = self.received.get(Pckt.Header.PacketNum)
                    if dup is not None:
                        return

                    # Dupe not found, so add to dictionary
                    self.received[Pckt.Header.PacketNum] = True

                    # Check if there is a jump in received packets
                    if Pckt.Header.PacketNum > self.previousPacketNum + 1:
                        for missed in range(self.previousPacketNum + 1, Pckt.Header.PacketNum):
                            print(f"Sending NACK for {Pckt.Header.PacketNum}\n")
                            self.send_NACK(missed)

                    # Increase top packet number recorded if necessary
                    if Pckt.Header.PacketNum > self.previousPacketNum:
                        self.previousPacketNum = Pckt.Header.PacketNum

                    # Mutex Lock to append packet to the buffer
                    with self.buffer_lock:
                        self.buffer.append(Pckt)
                    
            case packet.PacketType.ACK:
                print(f"Got ACK for {Pckt.Header.PacketNum}\n")
                # Received ACK for packet we sent
                with self.sending_lock:
                    # Register ACK
                    self.acks_for_sent[Pckt.Header.PacketNum] = True

            case packet.PacketType.NACK:
                print(f"Got NACK for {Pckt.Header.PacketNum}\n")
                # Received NACK for missing packet
                with self.sending_lock:
                    # Resend missing packet
                    self.send_packet(self.sliding_window[Pckt.Header.PacketNum])
            
            case packet.PacketType.SYN:
                print("Got SYN\n")
                self.send_SYNACK()
                
            case packet.PacketType.SYN_ACK:
                print("Got SYN_ACK\n")

            case _:
                print("Got Unrecognized Packet Type\n")


    def send_ACK(self, packNum: int):
        # Create ACK packet
        ack_packet = packet.Pckt(
            Header = packet.PcktHeader(
                Magic = globals.MAGIC,
                Checksum = 0,
                ConvID = globals.own_conv_id,
                PacketNum = packNum,
                SequenceNum = 0,
                Final = True,
                Type = packet.PacketType.ACK
            ),
            # empty byte array
            Body = bytearray()
        )
        # Send ACK packet
        self.send_packet(ack_packet)


    def send_NACK(self, packNum: int):
        # Create NACK packet
        nack_packet = packet.Pckt(
            Header = packet.PcktHeader(
                Magic = globals.MAGIC,
                Checksum = 0,
                ConvID = globals.own_conv_id,
                PacketNum = packNum,
                SequenceNum = 0,
                Final = True,
                Type = packet.PacketType.NACK
            ),
            # empty byte array
            Body = bytearray()
        )
        # Send NACK packet
        self.send_packet(nack_packet)    


    def send_SYN(self):
        # Create SYN packet
        syn_packet = packet.Pckt(
            Header = packet.PcktHeader(
                Magic = globals.MAGIC,
                Checksum = 0,
                ConvID = globals.own_conv_id,
                PacketNum = 0,
                SequenceNum = 0,
                Final = True,
                Type = packet.PacketType.SYN
            ),
            # empty byte array
            Body = bytearray()
        )
        # Send SYN packet
        self.send_packet(syn_packet)


    def send_SYNACK(self):
        # Create SYN packet
        syn_ack_packet = packet.Pckt(
            Header = packet.PcktHeader(
                Magic = globals.MAGIC,
                Checksum = 0,
                ConvID = globals.own_conv_id,
                PacketNum = 0,
                SequenceNum = 0,
                Final = True,
                Type = packet.PacketType.SYN_ACK
            ),
            # empty byte array
            Body = bytearray()
        )
        # Send SYN_ACK packet
        self.send_packet(syn_ack_packet)


    def send_HelloPckt(self):
        # Get a new Sequence number
        with self.sr_function_lock:
            
            # Create Hello Pckt packet
            hello_packet = packet.Pckt(
                Header = packet.PcktHeader(
                    Magic = globals.MAGIC,
                    Checksum = 0,
                    ConvID = globals.own_conv_id,
                    PacketNum = self.largestPacketNum,
                    SequenceNum = 0,
                    Final = True,
                    Type = packet.PacketType.Data
                ),
                Body = consensus.encode_Hello(
                    consensus.PcktHello(
                        DataID = consensus.PcktID.hello_c2s,
                        Version = 0,
                        NumFeatures = 1,
                        Feature = [1]
                    )
                )
            )

            self.sliding_window[self.largestPacketNum] = hello_packet
            self.largestPacketNum += 1


    def send_HelloBackPckt(self):
        # Get a new Sequence number
        with self.sr_function_lock:
            
            # Create HelloBack Pckt packet
            helloback_packet = packet.Pckt(
                Header = packet.PcktHeader(
                    Magic = globals.MAGIC,
                    Checksum = 0,
                    ConvID = globals.own_conv_id,
                    PacketNum = self.largestPacketNum,
                    SequenceNum = 0,
                    Final = True,
                    Type = packet.PacketType.Data
                ),
                Body = consensus.encode_HelloResponse(
                    consensus.PcktHelloResponse(
                        DataID = consensus.PcktID.hello_back_s2c,
                        Version = 0,
                        NumFeatures = 1,
                        Feature = [1]
                    )
                )
            )

            self.sliding_window[self.largestPacketNum] = helloback_packet
            self.largestPacketNum += 1

    
    def send_VoteRequest(self, voteID : uuid.UUID, question : str):
        with self.sr_function_lock:

            # Create VoteRequest Packet
            vote_request_packet = packet.Pckt(
                Header = packet.PcktHeader(
                    Magic = globals.MAGIC,
                    Checksum = 0,
                    ConvID = globals.own_conv_id,
                    PacketNum = self.largestPacketNum,
                    SequenceNum = 0,
                    Final = True, # this might be incorrect, depends on fragmentation
                    Type = packet.PacketType.Data
                ),
                Body = consensus.encode_VoteRequest(
                    consensus.PcktVoteRequest(
                        DataID = consensus.PcktID.vote_c2s_request_vote,
                        VoteID = voteID,
                        QuestionLength = len(question),
                        Question = question
                    )
                )
            )

            self.sliding_window[self.largestPacketNum] = vote_request_packet
            self.largestPacketNum += 1


    def send_VoteBroadcast(self, voteID : uuid.UUID, question : str):
        with self.sr_function_lock:
            vote_broadcast_packet = packet.Pckt(
                Header = packet.PcktHeader(
                    Magic = globals.MAGIC,
                    Checksum = 0,
                    ConvID = globals.own_conv_id,
                    PacketNum = self.largestPacketNum,
                    SequenceNum = 0,
                    Final = True,
                    Type = packet.PacketType.Data
                ),
                Body = consensus.encode_VoteBroadcast(
                    consensus.PcktVoteBroadcast(
                        DataID = consensus.PcktID.vote_s2c_broadcast_question,
                        VoteID = voteID,
                        QuestionLength = len(question),
                        Question = question
                    )
                )
            )

            self.sliding_window[self.largestPacketNum] = vote_broadcast_packet
            self.largestPacketNum += 1


    def send_VoteResponse(self, voteID : uuid.UUID, response : int):
        with self.sr_function_lock:
            vote_response_packet = packet.Pckt(
                Header = packet.PcktHeader(
                    Magic = globals.MAGIC,
                    Checksum = 0,
                    ConvID = globals.own_conv_id,
                    PacketNum = self.largestPacketNum,
                    SequenceNum = 0,
                    Final = True,
                    Type = packet.PacketType.Data
                ),
                Body = consensus.encode_VoteResponse(
                    consensus.PcktVoteResponse(
                        DataID = consensus.PcktID.vote_c2s_response_to_question,
                        VoteID = voteID,
                        Response = response 
                    )
                )
            )

            self.sliding_window[self.largestPacketNum] = vote_response_packet
            self.largestPacketNum += 1

    
    def send_BroadcastResult(self, voteID : uuid.UUID, result : int):
        with self.sr_function_lock:
            vote_result_packet = packet.Pckt(
                Header = packet.PcktHeader(
                    Magic = globals.MAGIC,
                    Checksum = 0,
                    ConvID = globals.own_conv_id,
                    PacketNum = self.largestPacketNum,
                    SequenceNum = 0,
                    Final = True,
                    Type = packet.PacketType.Data
                ),
                Body = consensus.encode_ResultBroadcast(
                    consensus.PcktVoteResultBroadcast(
                        DataID = consensus.PcktID.vote_s2c_broadcast_result,
                        VoteID = voteID,
                        Response = result
                    )
                )
            )

            self.sliding_window[self.largestPacketNum] = vote_result_packet
            self.largestPacketNum += 1
    

    def send_packet(self, Pckt: packet.Pckt):
        # Encode packet into bytearray
        packet_bytearray = bytearray(packet.encode_packet(Pckt))

        # Generate Checksum for packet_bytearray
        packet_bytearray[4:8] = struct.pack('!I', zlib.crc32(packet_bytearray[8:]))

        # If this a Data Type packet we are sending, perform the appropriate checks
        if Pckt.Header.Type == packet.PacketType.Data:
            with self.sending_lock:
                # Check if has been sent before
                acked = self.acks_for_sent.get(Pckt.Header.PacketNum)
                if acked is not None:
                    # Check if has been acked already
                    if acked == True:
                        # ACKed already, so don't send
                        return

                # Create or Restart Timer if necessary, saving the current time in ms (don't ask why this works)
                self.timers[Pckt.Header.PacketNum] = int(time.time() * 1000)

                # Set ACK received state to false
                self.acks_for_sent[Pckt.Header.PacketNum] = False

        # Send packet to receiving node (with 25% chance it will get lost)
        if random.randint(0, 3) == 1:
            print(f"Packet Sequence Number: {Pckt.Header.SequenceNum} will be lost\n")
        else:
            globals.own_socket.sendto(bytes(packet_bytearray), self.client_address)


    # This loops through the acks_for_sent dictionary, resending un-ACKed packets that have timed out
    def resend_manager(self):
        with self.sr_function_lock:
            # Loop through dictionary for any packets with an ACKed status that is false
            for PacketNum in self.acks_for_sent:
                if self.acks_for_sent[PacketNum] == False:
                    # Check if we have waited long enough (500ms)
                    if int(time.time() * 1000) - self.timers[PacketNum] > 500:
                        # Resend packet
                        print(f"Resending Packet {PacketNum}\n")
                        self.send_packet(self.sliding_window[PacketNum])


    # This moves the sliding window
    def slide_window(self):
        # Check to make sure no packets were skipped
        with self.sr_function_lock:
            for PackNum in range(1, self.windowBottom):
                if self.sliding_window.get(PackNum) is not None:
                    if self.acks_for_sent.get(PackNum) is not None:
                        if self.acks_for_sent[PackNum] == False:
                            print(f"Didn't get ACK for packet num: {PackNum}")
                            time.sleep(10)


        # Update window bottom
        with self.sr_function_lock:
            # Save the original window bottom for the for-loop
            old_windowBottom = self.windowBottom

            # Move the window
            for PackNum in range(old_windowBottom, old_windowBottom + self.windowSize):
                # Check if the packet with the PackNum actually exists
                if self.sliding_window.get(PackNum) is not None:
                    # Check if it has been sent
                    if self.acks_for_sent.get(PackNum) is not None:
                        # Check if it has been ACKed
                        if self.acks_for_sent[PackNum] == True:
                            # If ACKed, we can move the window
                            self.windowBottom += 1
                        else:
                            # We have to stop here, window can't be moved
                            break
            
            # Send not-yet-sent Packets within window
            for PackNum in range(self.windowBottom, self.windowBottom + self.windowSize):
                # Check if the packet with the PackNum actually exists
                if self.sliding_window.get(PackNum) is not None:
                    # Check if it has been sent
                    if self.acks_for_sent.get(PackNum) is not None:
                        return
                    else:
                        # It hasn't been sent so send it
                        #print(f"Sending packet with Number: {PackNum}.\n")
                        self.send_packet(self.sliding_window[PackNum])
                else:
                    break


    # This main loop is running on the object's own thread
    def main_loop(self):
        # Check for new messages
        while (self.main_loop_bool):
            time.sleep(0.2)

            with self.buffer_lock:
                if len(self.buffer) > 0:

                    # Get and Check ID
                    match consensus.decode_pcktID(self.buffer[0].Body):
                        case consensus.PcktID.hello_c2s:
                            print(f"Got Hello Packet with Packet Number: {self.buffer[0].Header.PacketNum} from {self.buffer[0].Header.ConvID}.\n")

                            # Send HelloBack
                            self.send_HelloBackPckt()

                        case consensus.PcktID.hello_back_s2c:
                            print(f"Got Hello Back Packet with Packet Number: {self.buffer[0].Header.PacketNum} from {self.buffer[0].Header.ConvID}.\n")

                            # Send HelloBack
                            #self.send_HelloPckt()
                        
                        case consensus.PcktID.vote_c2s_request_vote:
                            print(f"Got Request Vote Packet with Packet Number: {self.buffer[0].Header.PacketNum} from {self.buffer[0].Header.ConvID}.\n")

                            # Server received VoteRequest Packet
                            # Create New Vote through VoteManager, to broadcast to other nodes
                            votePckt = consensus.decode_VoteRequest(self.buffer[0].Body)
                            globals.vote_manager_ref.startVote(votePckt)
                            

                        case consensus.PcktID.vote_s2c_broadcast_question:
                            print(f"Got Broadcast Question Packet with Packet Number: {self.buffer[0].Header.PacketNum} from {self.buffer[0].Header.ConvID}.\n")

                            # Client Node received Broadcast Question Packet
                            # Respond to Question
                            questionPckt = consensus.decode_VoteBroadcast(self.buffer[0].Body)
                            globals.vote_manager_ref.respondToQuestion(self, questionPckt)


                        case consensus.PcktID.vote_c2s_response_to_question:
                            print(f"Got Response to Question Packet with Packet Number: {self.buffer[0].Header.PacketNum} from {self.buffer[0].Header.ConvID}.\n")

                            # Server received Response to Question Packet from all nodes -> calls VoteManager
                            # Compute Consensus Response
                            responsePckt = consensus.decode_VoteResponse(self.buffer[0].Body)
                            globals.vote_manager_ref.computeResult(self.buffer[0].Header.ConvID, responsePckt)
                            

                        case consensus.PcktID.vote_s2c_broadcast_result:
                            print(f"Got Broadcast Result Packet with Packet Number: {self.buffer[0].Header.PacketNum} from {self.buffer[0].Header.ConvID}.\n")

                            # Client Node received Broadcast Result Packet
                            gotConsensus = consensus.decode_ResultBroadcast(self.buffer[0].Body)
                            globals.vote_manager_ref.receivedResult(gotConsensus)
                        
                        case _:
                            print("Got Unknown Data Type Packet")

                    # Remove Packet from buffer as we are done with it
                    self.buffer.pop(0)

            # Slide window
            if len(self.sliding_window) > 0 : self.slide_window()

            # Check if we have to resend anything / if any packets waiting on an ACK have timed out
            self.resend_manager()

            # Check if need to send SYN to verify node is still online (10s)
            if int(time.time() * 1000) - self.lastContact > 10000:
                self.missedCalls += 1
                self.send_SYN()
            
            # Check if we have reached 100 missed calls
            if self.missedCalls > 100:
                print("Marking for deletion")
                self.markedForDeletion = True
