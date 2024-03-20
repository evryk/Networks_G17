# Our UDP Protocol
This is what we have working so far...
 - A simple Server and Client system, where the client is able to send messages from the console indefinitely to the server, and the server sends back an ACK.
 - The Listener thread, started in the `server.py` file, listens for incoming packets. The first 4 bytes of each packet correspond to each client's unique ID.
 - The Listener Thread runs checks for pre-existing conversation objects. The conversation object's constructor starts a thread which manages all of the automated behaviour. The destructor will kill the thread.
 - Other threads are able to communicate between each other by mutex sending each other information using each thread's object's methods, for example, between the listener and a conversation thread.
 - The Listener thread is able to give the Client object packets by using the Class's internal receive_packet method, as in line 23 in `listener.py`: `conversation_object.receive_packet(string_data[4:])`, where the packet passed in the argument is stored inside the Class's buffer using a mutex lock to access it. This ensures the Class's main loop thread does not access the buffer at the same time.

### How to run
To run the server, run the command: `python3 ./UDP/server.py`

In another window, run the client: `python3 ./UDP/client.py`
- Type in a new message
- Loop goes on until terminated with *CTRL+C*

### Across the Internet
 - Server Address 0.0.0.0 means it's receiving from everywhere.
 - Change *"localhost"* in `client.py` to appropriate server IP address if sending to another device.