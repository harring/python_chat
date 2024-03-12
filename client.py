import socket
import threading
import json
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


# Handles incoming messages, decrypts using private key and prints result
def receive_messages(client, private_key):
    while True:
        try:
            encrypted_message = client.recv(1024)
            if encrypted_message:
                decrypted_message = private_key.decrypt(
                    encrypted_message,
                    padding.OAEP(
                        mgf = padding.MGF1(algorithm = hashes.SHA256()),
                        algorithm = hashes.SHA256(),
                        label = None
                    )
                )
                print(decrypted_message.decode('utf-8'))
        except Exception as e:
            print(f"Error receiving message: {e}")
            client.close()
            break

def prompt_user_for_info():
    server_ip = input("Enter the server IP address: ")
    server_port = input("Enter the server port: ")
    username = input("Enter your username: ")
    return server_ip, server_port, username


# Starts the client, makes sure keys exist and asks for server information
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Load server key
    with open('server_public_key.pem', 'rb') as key_file:
        server_public_key = serialization.load_pem_public_key(key_file.read())
    
      # Load private key
    with open('client_private_key.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password = None)

    config_path = 'user_config.json'

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        server_ip = config.get('server_ip')
        server_port = config.get('server_port')
        username = config.get('username')

        if not all([server_ip, server_port, username]):
            print("Config file is incomplete.")
            server_ip, server_port, username = prompt_user_for_info()

    else:
        print("Config file not found, please enter details manually.")
        server_ip, server_port, username = prompt_user_for_info()

    try:
        client.connect((server_ip, int(server_port)))
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return

    encrypted_username = server_public_key.encrypt(
        username.encode('utf-8'),
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )
    
    thread = threading.Thread(target=receive_messages, args=(client, private_key,))
    thread.daemon = True  # This ensures the thread exits when the main thread does
    thread.start()
    
    try:
        client.send(encrypted_username)  # Send the username to the server immediately after connecting
        while True:
            message = input("")
            if message == "/exit":
                break  # Break the loop to exit
            if message: 
                encrypted_message = server_public_key.encrypt(
                    message.encode('utf-8'),
                    padding.OAEP(
                        mgf = padding.MGF1(algorithm = hashes.SHA256()),
                        algorithm = hashes.SHA256(),
                        label = None
                    )
                )
                client.send(encrypted_message)
    finally:
        client.close()  # Ensure the client socket is closed properly

if __name__ == '__main__':
    start_client()
