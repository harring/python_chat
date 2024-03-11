import os
import socket
import threading
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Set up key directory


# List to keep track of all connected clients
clients = []

# Dictionary to map client connections to usernames
client_usernames = {}

# User keys
client_public_keys = {}

# Global flag to control the server's main loop
shutdown_server = False

# Set up server keys
private_key_path = 'private_key.pem'
public_key_path = 'public_key.pem'

# Set up user key directory
keys_dir = 'keys'
if not os.path.exists(keys_dir):
    os.makedirs(keys_dir)

if not (os.path.exists(private_key_path) and os.path.exists(public_key_path)):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    private_key_pem = private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.PKCS8,
        encryption_algorithm = serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("private_key.pem", "wb") as private_key_file:
        private_key_file.write(private_key_pem)

    with open("public_key.pem", "wb") as public_key_file:
        public_key_file.write(public_key_pem)

    print("New RSA keys generated")

else:
    with open(private_key_path, 'rb') as private_key_file:
        private_key_pem = private_key_file.read()

    with open(public_key_path, 'rb') as public_key_file:
        public_key_pem = public_key_file.read()

    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password = None
    )

    public_key = serialization.load_pem_public_key(public_key_pem)

    print("Existig RSA keys loaded")


def encrypt_message(message, user_public_key):
    encrypt_message = user_public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label=None
        )
    )
    return encrypt_message

def broadcast_encrypted_message(message, origin):
    """Sends a message to all clients except the origin."""
    for client in list(clients): 
        if client != origin:
            try:
                user_public_key = client_public_keys[client]
                encrypted_message = encrypt_message(message, user_public_key)
                client.send(encrypted_message)
            except Exception as e:
                print(f"Error encrypting or sending message to client: {e}")
                clients.remove(client)
                del client_usernames[client] 
                del client_public_keys[client]
                client.close()

def decrypt_message(encrypted_message, private_key):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )
    return decrypted_message.decode('utf-8')

def client_handler(connection):
    """Handles incoming messages from a client and broadcasts them."""
    global shutdown_server
    
    try:
        # The first message from the client will be their username
        encrypted_username = connection.recv(1024)
        username = decrypt_message(encrypted_username, private_key)
        key_path = os.path.join('keys', f"key_{username}.pem")
        if not os.path.exists(key_path):
            print(f"Key for {username} not found, declining connection.")
            connection.close()
            return
        with open(key_path, 'rb') as key_file:
            user_public_key = serialization.load_pem_public_key(key_file.read())
            client_usernames[connection] = username
            client_public_keys[connection] = user_public_key
            encrypted_welcome_message = encrypt_message("You have connected to the server", user_public_key)
            connection.send(encrypted_welcome_message)
    except Exception as e:
        print(f"Error receiving username: {e}")
        connection.close()
        return
    
    while True:
        try:
            encrypted_message = connection.recv(1024)
            decrypted_message = decrypt_message(encrypted_message, private_key)

            if decrypted_message == "/shutdown":
                print("Shutdown command received. Server is shutting down.")
                shutdown_server = True
                break
            if decrypted_message:
                full_message = f"{client_usernames[connection]}: {decrypted_message}"
                print(f"Received: {full_message}")
                broadcast_encrypted_message(full_message, connection)
        except Exception as e:
            print(f"Error: {e}")
            break
    
    clients.remove(connection)
    del client_usernames[connection]
    connection.close()

def start_server():
    """Starts the server and manages incoming connections."""
    global shutdown_server
    
    # Read the configuration from the JSON file
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        server_ip = config['server_ip']
        server_port = config['server_port']
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Use the IP and port from the configuration file
    server.bind((server_ip, server_port))
    server.settimeout(1)
    server.listen()
    
    print(f"Server started on {server_ip}:{server_port}. Listening for incoming connections...")  # Updated server started log

    try:
        while not shutdown_server:
            try:
                connection, address = server.accept()
                clients.append(connection)
                print(f"Connected to: {address}")
                thread = threading.Thread(target=client_handler, args=(connection,))
                thread.start()
            except socket.timeout:
                continue
    finally:
        for client in clients:
            client.close()
        server.close()
        print("Server has been shut down.")

if __name__ == '__main__':
    start_server()
