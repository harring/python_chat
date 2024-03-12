# Simple Python Chat Application with RSA Encryption

This Python chat application facilitates secure, real-time text communication between multiple clients through a central server. With simplicity and security as its core principles, it integrates RSA encryption to ensure end-to-end confidentiality and integrity of messages. The application utilizes Python's standard library, particularly socket and threading, for network connections and concurrent message handling, and includes RSA for robust security. The system is divided into two main components: client.py and server.py, each responsible for their specific functions within the chat ecosystem.

## Features
**Client-Side Script (client.py):** Enables users to securely connect to a chat server, send encrypted messages, and receive real-time updates from other clients. Users are prompted to enter the server IP address, port, and a username upon launch. The use of RSA encryption requires users to also manage cryptographic keys, enhancing the security of communications.

* Connection setup using IP address and port
* Username-based identification with encrypted submission
* Real-time, encrypted message sending and receiving
* Ability to exit the chat cleanly with /exit command
* RSA encryption for securing messages

**Server-Side Script (server.py):** Manages incoming client connections securely, encrypts and broadcasts messages to all clients except the sender, and supports encrypted server shutdown commands. It reads the server IP and port configuration from a config.json file and handles public key management for encryption.

* Handles multiple client connections with encrypted communication
* Broadcasts encrypted messages to all connected clients except the message origin
* Special /shutdown command for safe server shutdown, requiring encryption
* Client tracking and username association with RSA encryption
VSecure storage and management of client public keys for encryption
* Stores message history (last 100 messages by default) which the user can request by sending /history

## How It Works
1. **Server Initialization:**

* Start by running the server.py script. It will load the IP address and port settings from config.json and begin listening for incoming connections.
* The server handles each client connection in a separate thread, allowing for simultaneous message handling and broadcast.
* If no RSA keys can be found a pair is generated, the public key needs to be distributed to users.
* A directory named keys will be created if not existing, this is used to store users public keys in the format "key_username.pem".

2. **Client Connection:**

* Run client.py to start a client instance. The script prompts for the server's IP address, port, and a username. Alternatively the user can save their details in a file named "user_config.json" with the following format:

  `{
    "username" : "example_username",
    "server_ip" : "127.0.0.1",
    "server_port" : 5000
}`

* Once connected, clients can send messages to the chat, which are then broadcast to all other connected clients.
* Clients receive real-time messages from others until they decide to exit by typing /exit.
* Server public key and user private key is to be stored in the same directory as the script. These should be named: server_public_key.pem and client_private_key.pem

## Configuration
* Server Configuration (config.json): Before starting the server, ensure the config.json file contains the correct IP address and port number for the server.

  `{
  "server_ip": "127.0.0.1",
  "server_port": 5000
}`

## Running the Application
To run the server, navigate to the directory containing server.py and execute:


`python server.py`

For each client, in a separate terminal window, run:


`python client.py`

and follow the on-screen prompts to connect to the server.

## Requirements
* Python 3.x

* Standard Python libraries: socket, threading, json


## Enhanced Security with RSA Encryption Implementation

### Encryption Workflow:
* **User-to-Server Encryption:** When clients send messages to the server, these messages are encrypted using the server's public key. This ensures that only the server, which possesses the corresponding private key, can decrypt and read these messages.

* **Server-to-User Encryption:** The server encrypts outgoing messages or broadcasts using the client's public key before sending them out. This way, only the intended recipient, who has the matching private key, can decrypt and understand these messages.

### Key Management:
* **Public Key Registration:** Clients need to manually submit their public keys to the server (outside of this application). The server then stores these client public keys for future communication. This process ensures that the server can send encrypted messages to each client individually and that no unwanted users can connect.

* **Secure Server Communication:** The server's public key is distributed to clients securely (outside of this application). This public key is used by clients to encrypt their initial username submission and all subsequent messages.

### Goals for RSA Encryption Integration:
* **End-to-End Security:** Implement RSA encryption for all messages exchanged between the client and the server, ensuring that each message's confidentiality and integrity are preserved.

* **Key Management:** While the introduction of encryption adds complexity, this is made to ensure that only wanted users are able to connect to the server.

* **User Experience Considerations:**
Integrating RSA encryption requires users to manage cryptographic keys. While this adds a step to the initial setup, it's a critical component for securing communications. The application is designed to make this process as smooth as possible, but not providing guidance for key generation and setup.


## Project Background
This chat application is a hobby project created for the purposes of self-education and exploration in the field of network programming and cybersecurity. It serves as a practical platform to apply and deepen my understanding of programming concepts, socket communication, and encryption techniques.

This project is not intended for commercial use or as a fully-featured secure communication solution. It is a reflection of my passion for coding and a testament to the learning journey in software development and security.
