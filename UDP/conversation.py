import socket
import threading
import time
import packet

class conversation:
    def __init__(self, own_id):
        # Save the client ID
        self.conversation_id = own_id
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
        while (1):
            #time.sleep(1)

            with self.buffer_lock:
                if len(self.buffer) > 0:
                    print(f"Received from {self.conversation_id}: {self.buffer[0]}")

                    # Remove Packet from buffer as we are done with it
                    self.buffer.pop(0)


    # TCP-like functions will be defined here

    def handshake():
        pass

    class selective_repeat():
      def __init__(self, window_size, timeout):
        self.window_size = window_size;
        self.buffer = [None] * window_size # please initialize buffer here
        self.expected_seq_num = 0


      def send_packet(self, packet):
        pass
        # implement sending logic here

      def receive_packet(self, packet):
        seq_num = packet.Header.PcktID
        if seq_num == self.expected_seq_num:
          # Packet received in order
          self.buffer[seq_num % self.window_size] = packet
          self.expected_seq_num += 1
          self.send_ack(seq_num)
        else:
          pass
          # buffer here


      def send_ack(self, seq_num):
        ack_packet = PcktHeader(0, 0, seq_num)
        ack_packet_type = packet_types.get(seq_num)
        if ack_packet_type:
          ack_packet = ack_packet_type(ack_packet)
          self.send_packet(ack_packet)

     
#usage (sample, put this in driver file)

packet_types = {
    PcktID.hello_c2s.value: PcktHello,
    PcktID.hello_back_s2c.value = PcktHelloResponse,
    # add more types

}
        

    def tcp_cubic():
        pass
# Splitting up packet without fragmentation

    def fragmentator():
        pass
