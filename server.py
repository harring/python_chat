import socket
import threading
import json

# List to keep track of all connected clients
clients = []

# Dictionary to map client connections to usernames
client_usernames = {}

# Global flag to control the server's main loop
shutdown_server = False

def broadcast_message(message, origin):
    """Sends a message to all clients except the origin."""
    for client in list(clients): 
        if client != origin:
            try:
                client.send(message)
            except:
                clients.remove(client)
                del client_usernames[client] 
                client.close()

def client_handler(connection):
    """Handles incoming messages from a client and broadcasts them."""
    global shutdown_server
    
    try:
        # The first message from the client will be their username
        username = connection.recv(1024).decode('utf-8')
        client_usernames[connection] = username
    except Exception as e:
        print(f"Error receiving username: {e}")
    
    while True:
        try:
            message = connection.recv(1024).decode('utf-8')
            if message == "/shutdown":
                print("Shutdown command received. Server is shutting down.")
                shutdown_server = True
                break
                
            if message:
                full_message = f"{client_usernames[connection]}: {message}"
                print(f"Received: {full_message}")
                broadcast_message(full_message.encode('utf-8'), connection)
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
                connection.send("You have connected to the server".encode('utf-8'))  # Inform the user they've connected
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
