import socket
import time
import sys
from logger import logger

SERVER_HOST = '172.23.104.178'
SERVER_PORT = 9999

def connect_to_server():
    """Attempt to connect to the server and return the socket object."""
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            logger.info("Connected to server")
            return client_socket
        except socket.error as e:
            logger.info(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def main():
    if len(sys.argv) < 2:
        logger.info("Usage: python client.py <command>")
        return

    command = ' '.join(sys.argv[1:])

    client_socket = connect_to_server()

    while True:
        try:
            client_socket.send(command.encode())
            logger.info(f"Command '{command}' sent to the server.")
            break
        except socket.error as e:
            logger.info(f"Error sending command: {e}. Reconnecting...")
            client_socket = connect_to_server()
    
    # Receive the output from the server
    # output = client_socket.recv(4096).decode()
    # logger.info(output)
    
    client_socket.close()

if __name__ == "__main__":
    main()
