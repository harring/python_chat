import socket
import threading
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend



def receive_messages(client, private_key):
    while True:
        try:
            encrypted_message = client.recv(1024)
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

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Prompt the user for IP and port
    server_ip = input("Enter the server IP address: ")
    server_port = input("Enter the server port: ")
    
    try:
        server_port = int(server_port)  # Convert port to integer
    except ValueError:
        print("Error: Port must be a number")
        return  # Exit the function if the port is not a number
    
    try:
        client.connect((server_ip, server_port))  # Use the provided IP and port
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return  # Exit the function if connection fails
    
    with open('server_public_key.pem', 'rb') as public_key_file:
        server_public_key = serialization.load_pem_public_key(
            public_key_file.read(),
            backend  = default_backend()
        )
    
    with open('client_private_key.pem', 'rb') as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password = None
        )
    username = input("Enter your username: ")
    encrypted_username = server_public_key.encrypt(
        username.encode('utf-8'),
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )
    client.send(encrypted_username)

    
    thread = threading.Thread(target=receive_messages, args=(client, private_key,))
    thread.daemon = True  # This ensures the thread exits when the main thread does
    thread.start()
    
    try:
        client.send(encrypted_username)  # Send the username to the server immediately after connecting
        while True:
            message = input("")
            if message == "/exit":
                break  # Break the loop to exit
            if message:  # Only send if there's a message to avoid blank "You: "
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
