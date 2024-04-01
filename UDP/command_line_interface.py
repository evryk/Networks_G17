import sys
import globals
# Command line interface for client to call and request votes.

# Class containing the command line interfac, so that it can be called upon in the conversation file, this could be changed. 
class commandlineinterface:
    def __init__(self):
        self.question = None

# Help command, so the user knows how to request votes etc        
    def help_command(self):
        print("Command Golssary (Note: case sensitive):")
        print("-------------------------------------")
        print("If you wish to request a vote, type 'request vote' into the command and press enter.")
        print("If you wish to obtain your conversation ID, type 'id' into the command and press enter.")
        print("If you wish to exit the server, type 'quit' into the command line")
        print("-------------------------------------")
        self.run()

# Request a vote command
    def request_vote(self):
        print("Going to request a vote from the server, type your question here and then press Enter:")
        self.question = input()
        return
        # Placeholder for the packet to send accross to the server, this will be implemented in testing. 
        ###

# Quitting the server 
    def exit(self):
        print("Quitting the server...")
        sys.exit()

# Running the operation, this will be called from the conversation file to run the programme. 
    def run(self):
            while True:
                command = input("Enter a command (type 'Help' for command glossary): ")
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
                else:
                    print("Invalid command. Type 'Help' for command glossary.")

    def returnID(self):
        print(f"Your conversation ID is: ", globals.own_conv_id)
        self.run()
        
        