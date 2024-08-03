import socket
import time
import sys
from logger import logger

DEFAULT_SERVER_PORT = 52000
MAX_RETRIES = 1  # Maximum number of connection attempts

def connect_to_server(SERVER_HOST_IP, SERVER_PORT=DEFAULT_SERVER_PORT):
    """Attempt to connect to the server and return the socket object."""
    attempts = 0 
    while attempts < MAX_RETRIES:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST_IP, SERVER_PORT))
            logger.info("Connected to server")
            return client_socket
        except socket.error as e:
            attempts += 1
            logger.error(f"Connection attempt {attempts}/{MAX_RETRIES} failed: {e}. Retrying...")
            if attempts == MAX_RETRIES:
                logger.critical(f'Could not connect to server... Exiting')
                sys.exit(-1)

def main():
    if len(sys.argv) < 2:
        logger.info("Usage: python client.py <command>")
        return

    SERVER_HOST_IP, command = sys.argv[1], ' '.join(sys.argv[2:])
    logger.info(f'Attempting to send command:{command} to server IP:{SERVER_HOST_IP}')

    client_socket = connect_to_server(SERVER_HOST_IP)

    while True:
        try:
            client_socket.send(command.encode())
            logger.info(f"Command '{command}' sent to the server.")
            break
        except socket.error as e:
            logger.error(f"Error sending command: {e}. Reconnecting...")
            client_socket = connect_to_server()
        except KeyboardInterrupt:
            logger.error("Interrupted by user. Exiting...")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            break
    
    # Receive the output from the server
    # output = client_socket.recv(4096).decode()
    # logger.info(output)
    
    client_socket.close()

if __name__ == "__main__":
    main()
