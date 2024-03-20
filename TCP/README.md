# Our TCP Protocol
This is what we have working so far...
 - A simple Server and Client system, where the client is able to send messages from the console indefinitely to the server, and the server sends back an ACK.
 - Server Address 0.0.0.0 means it's receiving from everywhere.
 - Change *"localhost"* in ***client.py*** to appropriate server IP address if sending to another device.
 - Currently this code is working between devices on the same network, but not over the Internet.

### How to run
To run the server, run the command: ***python3 server.py***

In another window, run the client: ***python3 client.py***
- Type in a new message
- Loop goes on until terminated with *CTRL+C*