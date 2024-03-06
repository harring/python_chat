# Simple Python Chat Application

This simple Python chat application enables real-time text communication between multiple clients through a central server. Built with simplicity in mind, it leverages Python's standard library, particularly socket and threading, to handle network connections and concurrent message handling. The application is split into two main components: client.py and server.py, each handling their respective roles in the chat system.

## Features
Client-Side Script (client.py): Allows users to connect to a chat server, send messages, and receive real-time updates from other clients. The user is prompted to enter the server IP address, port, and a username upon launch.

Connection setup using IP address and port
Username-based identification
Real-time message sending and receiving
Ability to exit the chat cleanly with /exit command
Server-Side Script (server.py): Manages incoming client connections, broadcasts messages to all clients except the sender, and supports server shutdown through a special command. It reads server IP and port configuration from a config.json file.

Handles multiple client connections
Broadcasts messages to all connected clients except the message origin
Special /shutdown command for safe server shutdown
Client tracking and username association
## How It Works
1. **Server Initialization:**

* Start by running the server.py script. It will load the IP address and port settings from config.json and begin listening for incoming connections.
* The server handles each client connection in a separate thread, allowing for simultaneous message handling and broadcast.

2. **Client Connection:**

* Run client.py to start a client instance. The script prompts for the server's IP address, port, and a username.
* Once connected, clients can send messages to the chat, which are then broadcast to all other connected clients.
* Clients receive real-time messages from others until they decide to exit by typing /exit.

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

## Planned Features
### Enhanced Secure Messaging with RSA Encryption
A significant upgrade planned for the chat application is to enhance message security using RSA encryption. This improvement aims to bolster the confidentiality and integrity of the messages exchanged, employing an asymmetric encryption model where the server encrypts outgoing messages with its RSA private key, and users decrypt them with the corresponding public key.

Updated Encryption Workflow:
* **User-to-Server Encryption:** Users will continue to encrypt messages sent to the server using their own RSA private keys. The server, holding each user's public key, will decrypt these messages to verify authenticity and read the content.
* **Server-to-User Encryption:** For outgoing messages, the server will encrypt responses and broadcasts using its RSA private key. Clients, equipped with the server's public key, will be able to decrypt these messages, ensuring that messages are securely transmitted and can be authenticated as coming directly from the server.
* **Key Management and Registration:**
    * **Public Key Submission:** Users are required to submit their public keys to the server for initial setup. To enhance security, the addition of a new public key to the server's directory will require approval by the server administrator or host. This manual verification step ensures that only authorized users can communicate through the server.
    * **Server Key Distribution:** The server's public key will be distributed to users securely, allowing their clients to decrypt messages from the server. Strategies for secure key distribution could include direct transmission upon user validation or downloading from a secure, authenticated location.

**Goals for Implementation:**
* Integrate RSA encryption for both user-to-server and server-to-user message transmissions, ensuring end-to-end security.
* Develop a secure, administrative process for the submission and approval of user public keys, including mechanisms for key verification and acceptance.
* Modify the client and server applications to support the encryption and decryption processes, including handling the server's public key on the client side and managing user keys on the server side.
* Provide robust documentation and user guidance for managing RSA keys, including instructions for key generation, submission, and the secure acquisition of the server's public key.
### Impact and User Experience Considerations:
The introduction of RSA encryption for secure messaging will necessitate changes to the user experience, specifically in key management and the initial setup process. Users will need to generate RSA key pairs, submit their public keys for server approval, and securely obtain the server's public key. Although these steps add complexity to the user setup process, they are essential for achieving a higher level of security and trust within the chat application. Efforts will be made to streamline these processes and provide clear, user-friendly instructions and support.

## Project Background
This chat application is a hobby project created for the purposes of self-education and exploration in the field of network programming and cybersecurity. It serves as a practical platform to apply and deepen my understanding of programming concepts, socket communication, and encryption techniques.

This project is not intended for commercial use or as a fully-featured secure communication solution. It is a reflection of my passion for coding and a testament to the learning journey in software development and security.