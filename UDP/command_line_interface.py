import sys
# Command line interface for client to call and request votes.

# Class containing the command line interfac, so that it can be called upon in the conversation file, this could be changed. 
class commandlineinterface:
    def __init__(self):
        self.commands = {
            "Help": self.help_command(),
            "Request vote": self.request_vote(),
            "Quit": self.exitcommand(),
            "ID": self.returnID()
        }

# Help command, so the user knows how to request votes etc        
    def help_command(self):
        print("Command Golssary (Note: case sensitive):")
        print("If you wish to request a vote, type 'Request vote' into the command and press enter.")
        print("If you wish to obtain your conversation ID, type 'ID' into the command and press enter.")
        print("If you wish to exit the server, type 'Quit' into the command line")

# Request a vote command
    def request_vote(self):
        print("Going to request a vote from the server, type your question here:")

        vote_question = input()
        # Placeholder for the packet to send accross to the server, this will be implemented in testing. 
        ###

# Quitting the server 
    def exit(self):
        print("Quitting the server...")
        sys.exit()

# Running the operation, this will be called from the conversation file to run the programme. 
    def run(self):
        print("Welcome to the voting system! ")
        while True:
            command = input("Enter a command (type 'Help' for command glossary): ")
            if command in self.commands:
                self.commands[command]()
            else:
                print("Invalid command. Type 'Help' for command glossary.")

# Sample of what will be written into the main code. 
if __name__ == "__main__":
    cli = commandlineinterface()
    cli.run()
        
        