import sys
import globals
import uuid
import time
import threading

# Command line interface for client to call and request votes.

# Class containing the command line interface, so that it can be called upon in the conversation file, this could be changed. 
class commandlineinterface:
    def __init__(self):
        self.question = ""

        self.vote_lock = threading.Lock()

        cli_thread = threading.Thread(target=self.run, args=( ))
        self.display_welcome_once()
        cli_thread.start()

    # Help command, so the user knows how to request votes etc        
    def help_command(self):
        print("\n\nCommand Glossary (Note: case sensitive):")
        print("-----------------------------------------")
        print("If you wish to request a vote, type 'vote' into the command and press enter.")
        print("If you wish to send a Hello Packet, type 'hello' into the command and press enter")
        print("If you wish to obtain your conversation ID, type 'id' into the command and press enter.")
        print("If you wish to exit the server, type '", "\033[31m", "quit", "\033[37m","' into the command line")
        print("-----------------------------------------\n\n")

    # Request a vote command
    def request_vote(self):
        print("\nGoing to request a vote from the server, type your question here and then press Enter:")
        self.question = input()

        print(f"\nYour question is '", self.question, "', sending this to the server.\n")

        # Send Vote Request packet with our question 
        if len(self.question) != 0:
            for conv in globals.conversation_objects:
                globals.conversation_objects[conv].send_VoteRequest(uuid.uuid4(), self.question)

    def hello(self):
        print("Sending Hello Packet to server...")
        for conv in globals.conversation_objects:
            globals.conversation_objects[conv].send_HelloPckt()

    # Quitting the server, this will quit for the client.py file also
    def exit(self):
        print("\033[31m", "Quitting the server...")
        sys.exit()

    # Running the operation, this will be called from the conversation file to run the programme. 
    def run(self):
        with self.vote_lock:
            while True:
                time.sleep(5)
                command = input("Enter a command (type 'help' for command glossary): ")
                if command.lower() == "quit":
                    self.exit()
                    break
                elif command.lower() == "vote":
                    self.request_vote()
                elif command.lower() == "hello":
                    self.hello()
                elif command.lower() == "help":
                    self.help_command()
                elif command.lower() == "id":
                    self.returnID()
                else:
                    print("Invalid command. Type 'help' for command glossary.")

    # Returning the conversation ID to the client.
    def returnID(self):
        print(f"Your conversation ID is: {globals.own_conv_id}\n")

    def display_welcome_once(self):
        print("  V    V   OOO   TTTTT  IIIII  N   N  GGGGG    SSSS  Y   Y  SSSS  TTTTT  EEEEE  M   M")
        print("  V    V  O   O    T      I    NN  N  G       S       Y  Y  S       T    E      MM MM")
        print("  V    V  O   O    T      I    N N N  G  GG    SSS      Y     SSS   T    EEE    M M M")
        print("  VV  VV  O   O    T      I    N  NN  G   G      S     Y        S   T    E      M   M")
        print("   VVVV    OOO     T    IIIII  N   N   GGGG  SSSS     Y     SSSS    T    EEEEE  M   M\n\n")                                                       
        print("                        Welcome to the Voting System! \n\n")  

        
        