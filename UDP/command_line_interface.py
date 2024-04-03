import sys
import globals
# Command line interface for client to call and request votes.

# Class containing the command line interface, so that it can be called upon in the conversation file, this could be changed. 
class commandlineinterface:
    def __init__(self):
        self.question = ""

# Help command, so the user knows how to request votes etc        
    def help_command(self):
        print("Command Glossary (Note: case sensitive):")
        print("-------------------------------------")
        print("If you wish to request a vote, type 'request vote' into the command and press enter.")
        print("If you wish to obtain your conversation ID, type 'id' into the command and press enter.")
        #  print("If you wish to return the Server Address, type 'server address' into the command and press enter.")
        print("If you wish to exit the server, type '", "\033[31m", "quit", "\033[37m","' into the command line")
        print("-------------------------------------")
        self.run()

# Request a vote command
    def request_vote(self):
        print("Going to request a vote from the server, type your question here and then press Enter:")
        self.question = input()
        # return self.question
        # return
        # Placeholder for the packet to send accross to the server, this will be implemented in testing. 
        ###

# Quitting the server, this will quit for the client.py file also
    def exit(self):
        print("\033[31m", "Quitting the server...")
        sys.exit()

# Running the operation, this will be called from the conversation file to run the programme. 
    def run(self):
            while True:
                command = input("Enter a command (type 'help' for command glossary): ")
                if command.lower() == "quit":
                    self.exit()
                    break
                elif command.lower() == "request vote":
                    self.request_vote()
                    break
                elif command.lower() == "help":
                    self.help_command()
                elif command.lower() == "id":
                    self.returnID()
                #elif command.lower() == "server address":
                    #self.return_server_address()
                else:
                    print("Invalid command. Type 'Help' for command glossary.")

# Returning the conversation ID to the client.
    def returnID(self):
        print(f"Your conversation ID is: ", globals.own_conv_id)
        self.run()
    
    # def return_server_address(self):
    #     print(f"The server address is: ", globals.server_address)
    #     self.run()
    def go_to_client(self):
        self.display_welcome_once()
        self.run()

    def display_welcome_once(self):
        print("  V    V   OOO   TTTTT  IIIII  N   N  GGGGG    SSSS  Y   Y  SSSS  TTTTT  EEEEE  M   M")
        print("  V    V  O   O    T      I    NN  N  G       S       Y  Y  S       T    E      MM MM")
        print("  V    V  O   O    T      I    N N N  G  GG    SSS      Y     SSS   T    EEE    M M M")
        print("  VV  VV  O   O    T      I    N  NN  G   G      S     Y        S   T    E      M   M")
        print("   VVVV    OOO     T    IIIII  N   N   GGGG  SSSS     Y     SSSS    T    EEEEE  M   M\n\n")                                                       
        print("                        Welcome to the Voting System! \n\n")  

        
        