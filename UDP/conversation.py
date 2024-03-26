import socket
import threading
import time
import packet

class conversation:
    def __init__(self, own_id):
        # Save the client ID
        self.conversation_id = own_id
        # self.handshake_completed = False
        print(f"Conversation {self.conversation_id} created.")

        # This is where new packets arrive in the conversation
        self.buffer = []

        # Used with the buffer
        self.buffer_lock = threading.Lock()

        # Start main loop thread
        self.thread_reference = threading.Thread(target=self.main_loop, args=( ))
        self.thread_reference.start()
        
    def __del__(self):
        # Kill Thread
        self.thread_reference.join()

    def receive_packet(self, packet):
        # Mutex Lock to append packet to the buffer
        with self.buffer_lock:
            self.buffer.append(packet)


    # This main loop is running on the object's own thread
    def main_loop(self):
        # Check for new messages

        #self.handshake()

        while (1):
            time.sleep(1)

            with self.buffer_lock:
                if len(self.buffer) > 0:
                    print(f"Received from {self.conversation_id}: {self.buffer[0]}")

                    # Remove Packet from buffer as we are done with it
                    self.buffer.pop(0)


    # TCP-like functions will be defined here

    def handshake(self):
        
        #time.sleep(1)
        #print(f"Handshake initiated with {self.conversation_id}")
        #print("SYN")
        #time.sleep(1)
        #print("SYN-ACK")
        #time.sleep(1)
        #print("ACK")
        #print("Handshake completed")
        #self.handshake_completed = True
        pass

    def send_message(self, message):
        if not self.handshake_completed:
            print("Handshake not completed yet. Cannot send message.")
            return
        # Simulate sending message
        print(f"Message sent from {self.conversation_id}: {message}")
        pass

    def selective_repeat():
        pass

    def tcp_cubic():
        pass

    def fragmentator():
        pass