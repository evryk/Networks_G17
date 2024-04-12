# Our UDP Protocol
### Note
Please ensure you are using python 3.10 (to have match statement support), make sure you don't have python 3.12 specifically as there is a known bug regarding threading which won't allow the project to work. Use `python3 --version` to check your version.

When running the program, you will realise that client and server are experiencing packet loss. This is because we implemented a 25% chance that whatever is sent through our send_packet function in conversation.py gets lost. This way, you can clearly see how our selective repeat is working.

When requesting a vote as a client, make sure the question you send is of boolean format, eg. '2+2==4', '67 * 205==5367', '1 - 9837 < 209', '14 * 5 > 43'... 

### How to run
To run the server, run the command: `python3 server.py`

In another window, run the client: `python3 client.py`
- The client will continue to ping the server until it receives a conversation ID.
- The client sends a SYN, receives a SYN-ACK.
- The CLI then prompts the user/client with different options, one of them being to send a Vote Request...
- Write 'quit' to terminate a client.

### Across the Internet
 - Server Address 0.0.0.0 means it's receiving from everywhere.
 - Change *"localhost"* in `client.py` to appropriate server IP address if sending to another device.