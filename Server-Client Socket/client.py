import socket
import time
import sys

SERVER_HOST = 'localhost'
SERVER_PORT = 9999

def connect_to_server():
    """Attempt to connect to the server and return the socket object."""
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("Connected to server")
            return client_socket
        except socket.error as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <command>")
        return

    command = ' '.join(sys.argv[1:])

    client_socket = connect_to_server()

    while True:
        try:
            client_socket.send(command.encode())
            print(f"Command '{command}' sent to the server.")
            break
        except socket.error as e:
            print(f"Error sending command: {e}. Reconnecting...")
            client_socket = connect_to_server()
    
    # Receive the output from the server
    output = client_socket.recv(4096).decode()
    print(output)
    
    client_socket.close()

if __name__ == "__main__":
    main()
