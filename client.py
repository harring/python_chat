import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
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
    
    username = input("Enter your username: ")
    client.send(username.encode('utf-8'))  # Send the username to the server immediately after connecting
    
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True  # This ensures the thread exits when the main thread does
    thread.start()
    
    try:
        while True:
            message = input("")
            if message == "/exit":
                break  # Break the loop to exit
            if message:  # Only send if there's a message to avoid blank "You: "
                client.send(message.encode('utf-8'))
    finally:
        client.close()  # Ensure the client socket is closed properly

if __name__ == '__main__':
    start_client()
